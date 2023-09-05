use super::matched_states::get_next_superstate;
use super::{
    super::super::super::flow::{Flow, ResponseType, State},
    CStatusIn,
};

pub fn handle_noninitiative<'a>(ordered: &mut Vec<&'a str>, flow: &Flow<'a>, csi: &mut CStatusIn) {
    if csi.turns_since_initiative
        >= flow
            .superstates
            .iter()
            .find(|r| r.1.superstate_name == csi.superstate)
            .unwrap()
            .1
            .initiativeness
        && !ordered.iter().any(|state_name| {
            let full_state = flow
                .states
                .iter()
                .find(|checked_state| checked_state.1.state_name == *state_name)
                .unwrap()
                .1;
            matches!(full_state.state_type, ResponseType::Flexible)
                || matches!(full_state.state_type, ResponseType::Initiative)
        })
    {
        // there are no initiative or flexible, what do ?!?!
        // check remaining non-overiterated states from current state
        let current_superstatename = csi.superstate;
        let current_statenames = &flow
            .superstates
            .iter()
            .find(|superstate| superstate.1.superstate_name == current_superstatename)
            .unwrap()
            .1
            .states;
        let current_available_states: Vec<&State<'_>> = flow
            .states
            .iter()
            .filter(|state| {
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

        if current_available_states.is_empty() {
            println!("going off of the next superstate");
            // check first initiative state of next superstate - get_next_superstate() already exists
            let next_superstatename = get_next_superstate(flow, csi);
            let current_statenames = &flow
                .superstates
                .iter()
                .find(|superstate| superstate.1.superstate_name == next_superstatename)
                .unwrap()
                .1
                .states;
            let current_available_states: Vec<&State<'_>> = flow
                .states
                .iter()
                .filter(|state| {
                    current_statenames.contains(&state.1.state_name)
                        && (matches!(state.1.state_type, ResponseType::Flexible)
                            || matches!(state.1.state_type, ResponseType::Initiative))
                        && if let Some(usage) = csi.states_usage.get(state.1.state_name) {
                            state.1.iteration > *usage
                        } else {
                            // if state is not in usage, its iteration is 0, so it can be used
                            true
                        }
                })
                .map(|s| s.1)
                .collect();

            if current_available_states.is_empty() {
                // first state of next superstate, for when theres no init state, bad practice
                ordered.push(current_statenames[0])
            } else {
                // first initiative state of next superstate
                csi.turns_since_initiative = 0;
                ordered.push(current_available_states[0].state_name)
            }
        } else {
            csi.turns_since_initiative = 0;
            ordered.push(current_available_states[0].state_name);
        }

        /*
        println!(
            "debug\ncurrent statenames {:?}\ncurrent avaialable states {:?} ",
            current_statenames,
            current_available_states
                .iter()
                .map(|s| s.state_name)
                .collect::<Vec<&str>>()
        );
        */
    } else {
        csi.turns_since_initiative += 1;
        println!("missed a spot")
        //debug from here
    };
}
