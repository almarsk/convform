use super::super::Flow;
use super::handle_matched_states::is_given_response_type;
use super::initiative::handle_initiative;
use super::match_states::MatchItem;
use super::non_initiative::handle_noninitiative;
use super::response_states::ResponseStates;
use super::CStatusIn;
use crate::flow::ResponseType;

pub struct MatchedStates<'a> {
    matched_states: Vec<MatchItem<'a>>,
    pub c_status_in: CStatusIn<'a>,
}

impl<'a> MatchedStates<'a> {
    pub fn new(csi: CStatusIn<'a>, ms: Vec<MatchItem<'a>>) -> MatchedStates<'a> {
        MatchedStates {
            matched_states: ms,
            c_status_in: csi,
        }
    }
    pub fn get_states_and_csi(self) -> (Vec<MatchItem<'a>>, CStatusIn<'a>) {
        (self.matched_states, self.c_status_in)
    }

    pub fn get_usage(csi: &'a CStatusIn, state: &'a str) -> &'a usize {
        if let Some(usage) = csi.states_usage.get(state) {
            usage
        } else {
            &0
        }
    }
}

pub fn assess_response_states<'a>(
    mut response_states: Vec<&'a str>,
    mut csi: CStatusIn<'a>,
    flow: &'a Flow,
    superstate: Option<&'a str>,
) -> ResponseStates<'a> {
    //println!("response states: {:?}", response_states);
    let final_response_states: Vec<&'a str> = if !response_states.is_empty() {
        handle_initiative(response_states, flow, &mut csi)
    } else {
        println!("matched_states.rs line 45 -> fallback management needed\n");
        handle_noninitiative(&mut response_states, flow, &mut csi);
        response_states // THINK ABOUT THIS, THIS IS ALSO WHERE FALLBACK MANAGEMENT GOES
    };

    //println!("final response states: {:?}", final_response_states);

    let solo: Vec<&'a str> = final_response_states
        .iter()
        .filter(|state| is_given_response_type(state, flow, ResponseType::Solo))
        .copied()
        .collect();
    if !solo.is_empty() {
        //println!("goin solo");
        return ResponseStates::new(vec![solo[solo.len()]], csi, superstate);
    }

    ResponseStates::new(final_response_states, csi, superstate)
}
