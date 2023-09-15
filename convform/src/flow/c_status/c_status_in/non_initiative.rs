use super::handle_matched_states::get_next_superstate;
use super::{
    super::super::super::flow::{Flow, ResponseType, State},
    CStatusIn,
};

pub fn handle_noninitiative<'a>(
    ordered: &mut Vec<&'a str>,
    flow: &'a Flow<'a>,
    csi: &mut CStatusIn<'a>,
) {
    let is_time_to_be_initiative = csi.turns_since_initiative
        >= flow
            .superstates
            .iter()
            .find(|r| r.1.superstate_name == csi.superstate)
            .unwrap()
            .1
            .initiativeness;

    println!("init time: {}", is_time_to_be_initiative);

    if is_time_to_be_initiative {
        // check remaining non-overiterated states from current state
        let current_superstatename = csi.superstate;
        let current_statenames = &flow
            .superstates
            .iter()
            .find(|superstate| superstate.1.superstate_name == current_superstatename)
            .unwrap()
            .1
            .states;

        println!("current statenames: {:?}", current_statenames);

        let current_available_states: Vec<&State<'_>> = flow
            .states
            .iter()
            .filter(|state| {
                println!("usage: {:?}", csi.states_usage);

                if current_statenames.contains(&state.1.state_name) {
                    println!("current state: {}", state.1.state_name);
                    println!(
                        "is in: {}",
                        current_statenames.contains(&state.1.state_name)
                    );
                    println!(
                        "is init or flexi: {}",
                        (matches!(state.1.state_type, ResponseType::Flexible)
                            || matches!(state.1.state_type, ResponseType::Initiative))
                    );
                    println!(
                        "is nonoveriterated: {}",
                        if let Some(usage) = csi.states_usage.get(state.1.state_name) {
                            state.1.iteration > *usage
                        } else {
                            true
                        }
                    );
                }

                current_statenames.contains(&state.1.state_name)
                    && (matches!(state.1.state_type, ResponseType::Flexible)
                        || matches!(state.1.state_type, ResponseType::Initiative))
                    && if let Some(usage) = csi.states_usage.get(state.1.state_name) {
                        state.1.iteration > *usage
                    } else {
                        true
                    }
            })
            .map(|s| s.1)
            .collect();

        println!(
            "current availabel statenames: {:?}",
            current_available_states
                .iter()
                .map(|s| s.state_name)
                .collect::<Vec<&str>>()
        );

        if current_available_states.is_empty() {
            // check next superstate
            println!("current superstates offers no more states");
            off_to_next_superstate(flow, csi, ordered)
        } else {
            csi.turns_since_initiative = 0;
            ordered.push(current_available_states[0].state_name);
            println!("states after non_initiative: {:?}", ordered);
        }
    } else {
        csi.turns_since_initiative += 1;
        println!("almost missed a spot");
        off_to_next_superstate(flow, csi, ordered)
        //debug from here
    };
}

fn off_to_next_superstate<'a>(
    flow: &'a Flow<'a>,
    csi: &mut CStatusIn<'a>,
    ordered: &mut Vec<&'a str>,
) {
    println!("non_initiative.rs going off of the next superstate");
    // check first initiative state of next superstate - get_next_superstate() already exists
    let next_superstatename = get_next_superstate(flow, &csi.clone());
    let next_statenames = &flow
        .superstates
        .iter()
        .find(|superstate| superstate.1.superstate_name == next_superstatename)
        .unwrap()
        .1
        .states;
    let next_available_states: Vec<&State<'_>> = flow
        .states
        .iter()
        .filter(|state| {
            next_statenames.contains(&state.1.state_name)
                && (matches!(state.1.state_type, ResponseType::Flexible)
                    || matches!(state.1.state_type, ResponseType::Initiative)
                    || matches!(state.1.state_type, ResponseType::Solo))
                && if let Some(usage) = csi.states_usage.get(state.1.state_name) {
                    state.1.iteration > *usage
                } else {
                    // if state is not in usage, its iteration is 0, so it can be used
                    true
                }
        })
        .map(|s| s.1)
        .collect();

    if next_available_states.is_empty() {
        // first state of next superstate, for when theres no init state, bad practice
        ordered.push(next_statenames[0])
    } else {
        // first initiative state of next superstate
        csi.turns_since_initiative = 0;
        csi.superstate = get_next_superstate(flow, csi);
        ordered.push(next_available_states[0].state_name)
    }
}
