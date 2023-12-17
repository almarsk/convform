use super::super::flow::ResponseType::*;
use super::super::validate::helper_structs_validate::{are_same_variant, get_response_type};
use super::non_initiative::handle_noninitiative;
use super::{csi::CStatusIn, Flow};
use crate::flow::State;

pub fn handle_initiative<'a>(
    v: Vec<&'a str>,
    flow: &'a Flow<'a>,
    csi: &mut CStatusIn,
) -> Vec<&'a str> {
    //dbg!(v.clone());
    let (prioritized, non): (Vec<&'a str>, Vec<&'a str>) = v.into_iter().partition(|state| {
        flow.states
            .iter()
            .find(|s| &s.1.state_name == state)
            .unwrap()
            .1
            .prioritize
    });
    //dbg!(prioritized.clone(), non.clone());
    if prioritized.iter().any(|state_name| {
        are_same_variant(get_response_type(state_name, flow), &Initiative)
            || are_same_variant(get_response_type(state_name, flow), &Flexible)
    }) {
        order_responsive_and_first_init_plus_maybe_connective(prioritized, flow)
    } else {
        let mut ordered = prioritized.clone();
        ordered.extend(order_responsive_and_first_init_plus_maybe_connective(
            non, flow,
        ));

        if ordered.iter().any(|state_name| {
            are_same_variant(get_response_type(state_name, flow), &Initiative)
                || are_same_variant(get_response_type(state_name, flow), &Flexible)
                || are_same_variant(get_response_type(state_name, flow), &Solo)
        }) {
            csi.turns_since_initiative = 0;
        } else {
            crate::cnd_dbg!("managing noninitiative");
            handle_noninitiative(&mut ordered, flow, csi);
        };
        crate::cnd_dbg!(&ordered);
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

fn order_responsive_and_first_init_plus_maybe_connective<'a>(
    v: Vec<&'a str>,
    flow: &'a Flow<'a>,
) -> Vec<&'a str> {
    let mut last_init = ("", 0);
    let mut last_connective = ("", 0);

    //dbg!("v{v:?}");

    let mut acc = v.iter().rev().enumerate().fold(vec![], |mut acc, state| {
        match get_full_state(flow, state.1).state_type {
            Connective => {
                last_connective.0 = state.1;
                last_connective.1 = state.0;
            }
            Responsive => acc.push(*state.1),
            _ => {
                last_init.0 = state.1;
                last_init.1 = state.0
            }
        }

        acc
    });

    // put last initiative and possibly last connective at the end
    if !last_init.0.is_empty() {
        if last_init.1 < last_connective.1
            && last_connective.1 - last_init.1 == 1
            && !last_connective.0.is_empty()
        {
            //dbg!("pushin {:?} as the connective", last_connective.0);
            acc.push(last_connective.0);
            acc.push(last_init.0);
        } else {
            //dbg!("pushin {:?} as the initiative", last_init.0);
            acc.push(last_init.0);
        }
    };

    //dbg!("acc{acc:?}");
    acc
}
