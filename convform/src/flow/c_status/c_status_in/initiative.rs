use super::super::super::super::flow::ResponseType;
use super::handle_matched_states::is_given_response_type;
use super::non_initiative::handle_noninitiative;
use super::{CStatusIn, Flow};
use crate::flow::State;

pub fn handle_initiative<'a>(
    v: Vec<&'a str>,
    flow: &'a Flow<'a>,
    csi: &mut CStatusIn<'a>,
) -> Vec<&'a str> {
    //println!("coming into handle initiative {:?}", v);
    let (prioritized, non): (Vec<&'a str>, Vec<&'a str>) = v.into_iter().partition(|state| {
        flow.states
            .iter()
            .find(|s| &s.1.state_name == state)
            .unwrap()
            .1
            .prioritize
    });
    //println!("prio: {:?}, non: {:?}", prioritized, non);
    if prioritized.iter().any(|state_name| {
        is_given_response_type(state_name, flow, ResponseType::Initiative)
            || is_given_response_type(state_name, flow, ResponseType::Flexible)
    }) {
        order_responsive_and_last_init_plus_maybe_connective(prioritized, flow)
    } else {
        let mut ordered = prioritized.clone();
        ordered.extend(order_responsive_and_last_init_plus_maybe_connective(
            non, flow,
        ));

        if ordered.iter().all(|state_name| {
            println!("state name: {state_name}");

            !is_given_response_type(state_name, flow, ResponseType::Initiative)
                || !is_given_response_type(state_name, flow, ResponseType::Flexible)
                || !is_given_response_type(state_name, flow, ResponseType::Solo)
        }) {
            csi.turns_since_initiative = 0;
        } else {
            //csi.turns_since_initiative += 1;
            println!("managing noninitiative");
            handle_noninitiative(&mut ordered, flow, csi);
            println!("states out of noninitiative: {:?}", ordered);
        };
        //println!("ordered2 {:?}", ordered);
        ordered
    }
}

fn get_full_state<'a>(flow: &'a Flow<'a>, state_name: &'a str) -> &'a State<'a> {
    flow.states
        .iter()
        .find(|state| state.1.state_name == state_name)
        .unwrap()
        .1
}

fn order_responsive_and_last_init_plus_maybe_connective<'a>(
    v: Vec<&'a str>,
    flow: &'a Flow<'a>,
) -> Vec<&'a str> {
    println!("states coming into oralipmc {:?}", v);

    let mut last_init = ("", 0);
    let mut last_connective = ("", 0);

    let mut acc = v.iter().enumerate().fold(vec![], |mut acc, state| {
        match get_full_state(flow, state.1).state_type {
            ResponseType::Connective => {
                last_connective.0 = state.1;
                last_connective.1 = state.0;
            }
            ResponseType::Responsive => acc.push(*state.1),
            _ => {
                last_init.0 = state.1;
                last_init.1 = state.0
            }
        }

        acc
    });

    // put last initiative and possibly last connective at the end
    if !last_init.0.is_empty() {
        if last_init.1 > last_connective.1
            && last_init.1 - last_connective.1 == 1
            && !last_connective.0.is_empty()
        {
            println!("pushin {:?} as the connective", last_connective.0);
            acc.push(last_connective.0);
            acc.push(last_init.0);
        } else {
            println!("pushin {:?} as the initiative", last_init.0);
            acc.push(last_init.0);
        }
    };
    acc
}
