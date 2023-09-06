use super::super::Flow;
use super::initiative::handle_initiative;
use super::non_initiative::handle_noninitiative;
use super::response_states::ResponseStates;
use super::rhematize::rhematize;
use super::CStatusIn;
use crate::flow::ResponseType;
use linked_hash_set::LinkedHashSet;

#[allow(dead_code)]
#[derive(Clone, Debug)]
pub struct MatchItem<'a> {
    states: Vec<&'a str>,
    index_start: usize,
}

impl<'a> MatchItem<'a> {
    pub fn new(states: Vec<&'a str>, index_start: usize) -> Self {
        MatchItem {
            states,
            index_start,
        }
    }
    pub fn get_states(&self) -> &Vec<&'a str> {
        &self.states
    }
    pub fn get_index(&self) -> usize {
        self.index_start
    }
}

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

    fn get_usage(csi: &'a CStatusIn, state: &'a str) -> &'a usize {
        if let Some(usage) = csi.states_usage.get(state) {
            usage
        } else {
            &0
        }
    }

    // TODO out of matched states which will be used to compose?
    // TODO which checks will be performed here?
    // TODO which info to be passed to CStatusOut?
    //
    // if some of the matched states are in the next superstate and are initiative, only include those and change superstate
    //
    // if no states are flexible or responsive and turns_since_init > initiativness -> first init from the next superstate
    //
    // max says at once in routine take into account
    pub fn handle_matched_states(self, flow: &'a Flow) -> ResponseStates<'a> {
        let (matched_b4_rhem, csi) = self.get_states_and_csi();

        //println!("b4 rhem {:?}", matched_b4_rhem);

        let matched = rhematize(matched_b4_rhem);

        //println!("aftr rhem {:?}", matched);

        // check for solo states and return last solo one if there is some
        let solo: Vec<&'a str> = matched
            .iter()
            .filter(|state| check_rtype(state, flow, ResponseType::Solo))
            .copied()
            .collect();
        if !solo.is_empty() {
            //println!("goin solo");
            return assess_response_states(vec![solo[solo.len()]], csi, flow, None);
        }
        //
        //
        //
        // check if some matched states are from next superstate
        // and only return those if there are some
        let next_superstate = get_next_superstate(flow, &csi);
        let next_superstate_states = get_states_of_next_superstate(flow, next_superstate);
        let matches_next_superstate: Vec<&'a str> = matched
            .clone()
            .into_iter()
            .filter(|state| {
                check_rtype(state, flow, ResponseType::Initiative)
                    && next_superstate_states.contains(state)
            })
            .collect();
        if !matches_next_superstate.is_empty() {
            //println!("goin next superstate");
            return assess_response_states(
                matches_next_superstate,
                csi,
                flow,
                Some(next_superstate),
            );
        }
        //
        //
        //
        // filter overiterated out or return last overiterated if only overiterated
        let match_not_overiterated: Vec<&str> = matched
            .clone()
            .into_iter()
            .enumerate()
            .filter(|(i, ms)| {
                let next_state: Option<&str> = if matched.len() > i + 1 {
                    Some(matched[i + 1])
                } else {
                    None
                };

                let connective_next_check = if let Some(ns) = next_state {
                    let _ms_response_type = &flow
                        .states
                        .iter()
                        .find(|s| &s.1.state_name == ms)
                        .unwrap()
                        .1
                        .state_type;

                    if matches!(_ms_response_type, ResponseType::Connective) {
                        let no = not_overiterated(ns, flow, MatchedStates::get_usage(&csi, ns));
                        //println!("ns {} oi {}", ns, no);
                        no
                    } else {
                        true
                    }
                } else {
                    true
                };
                let no = not_overiterated(ms, flow, MatchedStates::get_usage(&csi, ms));
                //println!("no {current_no}");
                //println!("ns {} oi {}", ms, no);
                connective_next_check && no
            })
            .map(|(_, ms)| ms)
            //not overiterated and ALSO if connective before initiative, the initiative is also not overiterated
            .collect::<LinkedHashSet<_>>()
            .into_iter()
            .collect();
        println!("mno {:?}", match_not_overiterated);

        if match_not_overiterated.is_empty()
            || match_not_overiterated.iter().all(|s| {
                matches!(
                    flow.states
                        .iter()
                        .find(|state| state.1.state_name == *s)
                        .unwrap()
                        .1
                        .state_type,
                    ResponseType::Connective
                )
            })
        {
            if matched.is_empty() {
                // FALLBACK
                // println!("matched: {:#?}", matched);
                assess_response_states(vec![], csi, flow, None)
            } else {
                let matched_overiterated = matched;

                // LAST OVERITERATED RESPONSIVE
                if let Some(last) = matched_overiterated.iter().rev().find(|os| {
                    &flow
                        .states
                        .iter()
                        .find(|s| matches!(s.1.state_type, ResponseType::Responsive))
                        .unwrap()
                        .1
                        .state_name
                        == *os
                }) {
                    // println!("overiter1: {:#?}", matched_overiterated);
                    assess_response_states(vec![last], csi, flow, None)
                } else {
                    // println!("overiter2: {:#?}", matched_overiterated);
                    assess_response_states(vec![], csi, flow, None)
                }
            }
        } else {
            // println!("init handled nonover{:#?}", match_not_overiterated);
            // assess_response_states(rs, csi, flow)
            //println!("states passed in ars {:?}", match_not_overiterated);
            assess_response_states(match_not_overiterated, csi, flow, None)
        }
    }
}

fn not_overiterated(state: &str, flow: &Flow, usage: &usize) -> bool {
    if let Some(b) = &flow
        .states
        .iter()
        .find(|s| s.1.state_name == state)
        .map(|s| s.1.iteration)
    {
        //println!("iteration {b}");
        //println!("iteration fits {}", b > usage);
        b > usage
    } else {
        // println!("no iteration :(");
        false
    }
}

fn check_rtype(state: &str, flow: &Flow, _response_type: ResponseType) -> bool {
    if let Some(b) = flow
        .states
        .iter()
        .find(|(_, s)| s.state_name == state)
        .map(|(_, s)| !matches!(s.clone().state_type, _response_type))
    {
        b
    } else {
        false
    }
}

// in current routine find current superstate,
// then get the name of the next superstate (next of first if current is last)
// then check the initiative matched states against the next superstate
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

    if order_of_superstates.len() == index_current_superstate {
        order_of_superstates[0]
    } else {
        order_of_superstates[index_current_superstate + 1]
    }
}

fn get_states_of_next_superstate<'a>(flow: &'a Flow<'a>, superstate: &'a str) -> &'a Vec<&'a str> {
    &flow.superstates.get(superstate).unwrap().states
}

// assess_response_states(rs, csi, flow, superstate)
fn assess_response_states<'a>(
    mut response_states: Vec<&'a str>,
    mut csi: CStatusIn<'a>,
    flow: &'a Flow,
    superstate: Option<&'a str>,
) -> ResponseStates<'a> {
    //println!("{:?}", response_states);
    let final_response_states: Vec<&'a str> = if !response_states.is_empty() {
        //println!("dbg hi");
        handle_initiative(response_states, flow, &mut csi)
    } else {
        handle_noninitiative(&mut response_states, flow, &mut csi);
        response_states // THINK ABOUT THIS, THIS IS ALSOW WHERE FALLBACK MANAGEMENT GOES
                        // println!("matched_states.rs line 222 -> fallback management needed\n")
    };

    //println!("{:?}", final_response_states);

    let solo: Vec<&'a str> = final_response_states
        .iter()
        .filter(|state| check_rtype(state, flow, ResponseType::Solo))
        .copied()
        .collect();
    if !solo.is_empty() {
        //println!("goin solo");
        return ResponseStates::new(vec![solo[solo.len()]], csi, superstate);
    }

    ResponseStates::new(final_response_states, csi, superstate)
}
