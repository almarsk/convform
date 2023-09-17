use super::handle_matched_states::{get_next_superstate, is_given_response_type};
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

    if is_time_to_be_initiative {
        // check remaining non-overiterated states from current superstate
        let current_superstatename = csi.superstate;
        let current_statenames = &flow
            .superstates
            .iter()
            .find(|superstate| superstate.1.superstate_name == current_superstatename)
            .unwrap()
            .1
            .states;

        let current_available_states: Vec<&State<'a>> = current_statenames
            .iter()
            .filter(|state| {
                let f = is_given_response_type(state, flow, ResponseType::Flexible);
                let i = is_given_response_type(state, flow, ResponseType::Initiative);
                f || i
            })
            .map(|s| flow.states.iter().find(|state| state.0 == s).unwrap().1)
            .filter(|state| {
                if let Some(usage) = csi.states_usage.get(state.state_name) {
                    state.iteration > *usage
                } else {
                    true
                }
            })
            .collect();

        if current_available_states.is_empty() {
            // check next superstate
            off_to_next_superstate(flow, csi, ordered)
        } else {
            csi.turns_since_initiative = 0;
            ordered.push(current_available_states[0].state_name);
        }
    } else {
        csi.turns_since_initiative += 1;
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
