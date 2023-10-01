use crate::Flow;

use super::get_stringmatching_pool::GroupingInfo;
use super::matched_states::MatchedStates;
use super::CStatusIn;
use super::StringMatchingPool;
use itertools::Itertools;
use regex::Regex;

#[derive(Clone, Debug)]
pub struct MatchItem<'a> {
    _intent: &'a str,
    grouping: GroupingInfo<'a>,
    states: Vec<&'a str>,
    index_start: usize,
    answer_to: &'a [&'a str],
}

impl<'a> MatchItem<'a> {
    fn new(
        _intent: &'a str,
        grouping: GroupingInfo<'a>,
        states: Vec<&'a str>,
        index_start: usize,
        answer_to: &'a [&str],
    ) -> Self {
        MatchItem {
            _intent,
            grouping,
            states,
            index_start,
            answer_to,
        }
    }
    pub fn get_states(&self) -> Vec<&'a str> {
        self.states.clone()
    }
    pub fn get_index(&self) -> usize {
        self.index_start
    }
}

impl<'a> StringMatchingPool<'a> {
    pub fn match_states(self, flow: &'a Flow) -> MatchedStates<'a> {
        let mut csi = self.get_csi();
        let user_reply = csi.view_user_reply();
        let kaps = self.get_kaps(); // decompose combined intents

        // check if beginning of conversation - return state intro
        if csi.view_user_reply().is_empty() {
            let csi = CStatusIn::default().treat(flow);
            // beginning of conversation
            MatchedStates::new(
                csi,
                vec![MatchItem::new(
                    "",
                    GroupingInfo::default(),
                    vec!["state_intro"],
                    0,
                    &[],
                )],
            )
        } else {
            // each ToMatch in kaps needs to be check against the user_reply
            let match_items: Vec<MatchItem<'a>> = kaps
                .clone()
                .into_iter()
                .filter_map(|kap| {
                    let mut start_index = usize::MAX;
                    // each keyword in each ToMatch needs to be checked against the user_reply
                    if kap.keywords().iter().any(|kw| {
                        let kw_rgx = Regex::new(&format!("(?i){}", kw)).unwrap();
                        let captures_vec: Vec<_> = kw_rgx.captures_iter(user_reply).collect();
                        let is_match = !captures_vec.is_empty();

                        // determine the earliest start index
                        for cap in captures_vec {
                            let current_start_index = cap.get(0).unwrap().start();
                            if current_start_index < start_index {
                                start_index = current_start_index
                            }
                        }

                        is_match
                    }) {
                        Some(MatchItem::new(
                            kap.intent_name,
                            kap.grouping,
                            kap.adjacent,
                            start_index,
                            kap.answer_to,
                        ))
                    } else {
                        None
                    }
                })
                .collect::<Vec<MatchItem<'a>>>();

            let unfiltered_sufficing_match_items: Vec<MatchItem<'a>> = match_items
                .clone()
                .into_iter()
                .filter(|mi| {
                    let req_amount = mi.grouping.number;
                    let req_id = mi.grouping.id;

                    // make sure that all the required intents for composed intent are matched
                    match_items
                        .iter()
                        .filter(|mi_req| mi_req.grouping.id == req_id)
                        .count()
                        == req_amount
                })
                .collect();

            let sufficing_match_items: Vec<MatchItem<'a>> = unfiltered_sufficing_match_items
                .clone()
                .into_iter()
                .filter(|mi| {
                    let req_amount = mi.grouping.number;
                    let req_id = mi.grouping.id;

                    // make sure that between identical intent names the composed one overrides
                    !unfiltered_sufficing_match_items.iter().any(|mi_req| {
                        mi_req._intent == mi._intent
                            && req_amount < mi_req.grouping.number
                            && req_id != mi_req.grouping.id
                    })
                })
                .collect();

            let mut recomposed_match_items: Vec<MatchItem<'a>> = vec![];
            let regrouped = sufficing_match_items.iter().group_by(|i| i.grouping.id);

            for (_, group) in regrouped.into_iter() {
                let group_vec: Vec<_> = group.collect();
                let count = group_vec.len();

                if count == 1 {
                    recomposed_match_items.push(group_vec[0].clone())
                } else {
                    let intent_names: Vec<&'a str> = group_vec.iter().map(|g| g._intent).collect();
                    let origin_state: &'a str = group_vec[0].grouping.origin;
                    let recomposed_intent_full = flow
                        .states
                        .iter()
                        .find(|s| s.0 == &origin_state)
                        .unwrap()
                        .1
                        //actually need to check intents of last states
                        .intents
                        .iter()
                        .find(|i| {
                            intent_names.iter().all(|im| {
                                i.0.contains(format!("+{im}").as_str())
                                    || i.0.contains(format!("{im}+").as_str())
                            })
                        })
                        .unwrap();

                    let recomposed_intent = MatchItem::new(
                        recomposed_intent_full.0,
                        group_vec[0].grouping.clone(),
                        recomposed_intent_full.1.clone(),
                        group_vec.iter().map(|g| g.index_start).min().unwrap(),
                        &[],
                    );

                    recomposed_match_items.push(recomposed_intent)
                }
            }

            // fuse back decomposed combined matchitems
            // each main one - check if the empty ones are there
            // if all of them -
            //              fuse => intent name intent1+intent2...
            //                      adjacent just on the main one
            //                      the lowest start index
            //                      all answer to s can be fused,
            //                          because duplicity check has
            //                          been done upon decompose

            // increment implicitly answered states usage
            recomposed_match_items.iter().for_each(|k| {
                k.answer_to.iter().for_each(|at| {
                    let new_state_usage = csi.states_usage.entry(*at).or_insert(0);
                    *new_state_usage += 1;
                })
            });

            MatchedStates::new(csi, recomposed_match_items)
        }
    }
}
