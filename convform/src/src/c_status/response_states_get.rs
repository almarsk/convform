use super::super::flow::{the_track::next_from_the_track, ResponseType};
use super::super::validate::helper_structs_validate::{are_same_variant, get_response_type};
use super::matched_states::{MatchItem, MatchedStates};
use super::response_states::ResponseStates;
use super::stringmatching_pool::GroupingInfo;
use super::CStatusIn;
use super::Flow;
use super::{initiative::handle_initiative, non_initiative::handle_noninitiative};
use linked_hash_set::LinkedHashSet;

impl<'a> MatchedStates<'a> {
    pub fn get_response_states(self, flow: &'a Flow) -> ResponseStates<'a> {
        let (mut matched_b4_rhem, mut csi) = self.get_states_and_csi();

        if csi.bot_turns == 0 {
            matched_b4_rhem.push(MatchItem::new(
                "",
                GroupingInfo {
                    id: 0,
                    number: 1,
                    origin: "",
                },
                vec!["state_intro"],
                0,
                &[],
            ))
        }

        crate::cnd_dbg!(&csi.states_usage);

        if matched_b4_rhem.is_empty() {
            /*
                if
                // csi.fallback ||   --> comes into play with gpt intent reco
            {
                // FALLBACK
                crate::cnd_dbg!("empty matched states case needs handling");
                todo!("fallback gpt autopilot time")
            } else {
            */
            // next from the track
            crate::cnd_dbg!("assessing matched states next from the track");
            let mut next_state_vec: Vec<&'a str> = vec![];
            if let Some(next_state) = next_from_the_track(flow, &mut csi) {
                next_state_vec.push(next_state);
            }
            return assess_response_states(next_state_vec, csi, flow);
            //}
        }
        crate::cnd_dbg!(&matched_b4_rhem);

        // order states by start index + converts MatchItems into &strs
        let matched = rhematize(matched_b4_rhem);

        // check for solo states and return last solo one if there is some
        let solo: Vec<&'a str> = matched
            .iter()
            .filter(|state| are_same_variant(get_response_type(state, flow), &ResponseType::Solo))
            .copied()
            .collect();
        if !solo.is_empty() {
            let last_solo_to_vec = vec![solo[solo.len() - 1]];
            crate::cnd_dbg!("assessing matched states solo");
            return assess_response_states(last_solo_to_vec, csi, flow);
        };

        // get non-overiterated states
        let nonoveriterated: Vec<&'a str> = matched
            .clone()
            .into_iter()
            .enumerate()
            .filter(|(i, ms)| {
                postcedent_state_to_connective_unoveriterated(i, matched.clone(), &csi, flow)
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
            crate::cnd_dbg!("assessing matched states all overiterated");
            return assess_response_states(vec![last_overiterated], csi, flow);
        }
        crate::cnd_dbg!("assessing matched states happy path");
        assess_response_states(nonoveriterated, csi, flow)
    }
}

pub fn assess_response_states<'a>(
    mut response_states: Vec<&'a str>,
    mut csi: CStatusIn,
    flow: &'a Flow,
) -> ResponseStates<'a> {
    //dbg!(response_states);
    let final_response_states: Vec<&'a str> = if !response_states.is_empty() {
        handle_initiative(response_states, flow, &mut csi)
    } else {
        crate::cnd_dbg!("fallback management needed");
        handle_noninitiative(&mut response_states, flow, &mut csi);
        response_states // THINK ABOUT THIS, THIS IS ALSO WHERE FALLBACK MANAGEMENT GOES
    };

    crate::cnd_dbg!(&final_response_states);

    let solo: Vec<&'a str> = final_response_states
        .iter()
        .filter(|state| are_same_variant(get_response_type(state, flow), &ResponseType::Solo))
        .copied()
        .collect();
    if !solo.is_empty() {
        //dbg!("goin solo");
        return ResponseStates::new(vec![solo[solo.len() - 1]], csi);
    }

    ResponseStates::new(final_response_states, csi)
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

fn postcedent_state_to_connective_unoveriterated(
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
        if are_same_variant(get_response_type(ns, flow), &ResponseType::Connective) {
            let no = !is_overiterated(ns, flow, MatchedStates::get_usage(csi, ns));
            //dbg!("ns {} oi {}", ns, no);
            no
        } else {
            true
        }
    } else {
        true
    }
}

pub fn rhematize(mut m: Vec<MatchItem<'_>>) -> Vec<&'_ str> {
    let _ = &mut m.sort_by_key(|ms| ms.get_index());
    m.into_iter()
        .flat_map(|m| m.get_states().to_vec())
        .collect()
}
