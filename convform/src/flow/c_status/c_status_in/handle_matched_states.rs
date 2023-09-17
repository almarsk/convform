use super::super::super::ResponseType;
use super::matched_states::assess_response_states;
use super::matched_states::MatchedStates;
use super::response_states::ResponseStates;
use super::rhematize::rhematize;
use super::CStatusIn;
use super::Flow;
use linked_hash_set::LinkedHashSet;

impl<'a> MatchedStates<'a> {
    pub fn handle_matched_states2(self, flow: &'a Flow) -> ResponseStates<'a> {
        let (matched_b4_rhem, csi) = self.get_states_and_csi();

        //println!("usage at start of handle: {:?}", csi.states_usage);

        if matched_b4_rhem.is_empty() {
            // FALLBACK
            // println!("matched: {:#?}", matched);
            //println!("asss because empty");
            return assess_response_states(vec![], csi, flow, None);
        }

        // order states by start index
        let matched = rhematize(matched_b4_rhem);

        // check for solo states and return last solo one if there is some
        let solo: Vec<&'a str> = matched
            .iter()
            .filter(|state| is_given_response_type(state, flow, ResponseType::Solo))
            .copied()
            .collect();
        if !solo.is_empty() {
            let last_solo_to_vec = vec![solo[solo.len() - 1]];
            //println!("asss because solo");
            return assess_response_states(last_solo_to_vec, csi, flow, None);
        };

        // check if some matched states are from next superstate
        // and only return those if there are some
        let next_superstate = get_next_superstate(flow, &csi);
        let next_superstate_states = &flow.superstates.get(next_superstate).unwrap().states;
        let matches_next_superstate: Vec<&'a str> = matched
            .clone()
            .into_iter()
            .filter(|state| {
                is_given_response_type(state, flow, ResponseType::Initiative)
                    && next_superstate_states.contains(state)
            })
            .collect();
        if !matches_next_superstate.is_empty() {
            //println!("goin next superstate");
            //println!("asss because next superstate match");
            return assess_response_states(
                matches_next_superstate,
                csi,
                flow,
                Some(next_superstate),
            );
        }

        // get non-overiterated states
        let nonoveriterated: Vec<&'a str> = matched
            .clone()
            .into_iter()
            .enumerate()
            .filter(|(i, ms)| {
                antecedent_state_to_connective_unoveriterated(i, matched.clone(), &csi, flow)
                    && !is_overiterated(ms, flow, MatchedStates::get_usage(&csi, ms))
            })
            .map(|(_, ms)| ms)
            //not overiterated and ALSO if connective before initiative, the initiative is also not overiterated
            .collect::<LinkedHashSet<_>>()
            .into_iter()
            .collect();

        if nonoveriterated.is_empty() {
            let matched_overiterated = matched;
            let last_overiterated = matched_overiterated.iter().last().unwrap();
            //println!("asss because last overiterated");
            return assess_response_states(vec![last_overiterated], csi, flow, None);
        }
        //println!("asss happy path");
        assess_response_states(nonoveriterated, csi, flow, None)
    }
}

pub fn is_given_response_type(state: &str, flow: &Flow, response_type: ResponseType) -> bool {
    if let Some(b) = flow.states.iter().find(|(_, s)| s.state_name == state).map(|(_, s)| {
        std::mem::discriminant(&s.clone().state_type) == std::mem::discriminant(&response_type)
    }) {
        b
    } else {
        println!("cant check response type - state not found");
        false
    }
}

pub fn get_next_superstate<'a>(flow: &'a Flow, csi: &CStatusIn) -> &'a str {
    let order_of_superstates = &flow
        .routines
        .iter()
        .find(|r| r.1.routine_name == csi.routine)
        .map(|r| r.1)
        .unwrap()
        .order_superstates;

    let index_current_superstate = order_of_superstates
        .iter()
        .position(|s| s == &csi.superstate)
        .unwrap();

    if order_of_superstates.len() <= index_current_superstate {
        order_of_superstates[0]
    } else {
        order_of_superstates[index_current_superstate + 1]
    }
}

fn is_overiterated(state: &str, flow: &Flow, usage: &usize) -> bool {
    if let Some(allowed_iteration) = &flow
        .states
        .iter()
        .find(|s| s.1.state_name == state)
        .map(|s| s.1.iteration)
    {
        allowed_iteration <= usage
    } else {
        false
    }
}

fn antecedent_state_to_connective_unoveriterated(
    i: &usize,

    matched: Vec<&str>,
    csi: &CStatusIn,
    flow: &Flow,
) -> bool {
    let next_state: Option<&str> = if matched.len() > i + 1 {
        Some(matched[i + 1])
    } else {
        None
    };
    if let Some(ns) = next_state {
        if is_given_response_type(ns, flow, ResponseType::Connective) {
            let no = !is_overiterated(ns, flow, MatchedStates::get_usage(csi, ns));
            //println!("ns {} oi {}", ns, no);
            no
        } else {
            true
        }
    } else {
        true
    }
}
