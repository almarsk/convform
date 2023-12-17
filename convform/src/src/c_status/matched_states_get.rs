use super::matched_states::MatchItem;
use super::matched_states::MatchedStates;
use super::stringmatching_pool::StringMatchingPool;
use super::Flow;
use itertools::Itertools;
use regex::Regex;

impl<'a> StringMatchingPool<'a> {
    pub fn get_matched_states(self, flow: &'a Flow) -> MatchedStates<'a> {
        let mut csi = self.csi;
        let user_reply = csi.user_reply.clone();
        let kaps = self.keywords_adjacent_pairs; // decompose combined intents

        crate::cnd_dbg!(&kaps);

        // each ToMatch in kaps needs to be check against the user_reply
        let match_items: Vec<MatchItem<'a>> = kaps
            .clone()
            .into_iter()
            .filter_map(|kap| {
                let mut start_index = usize::MAX;
                // each keyword in each ToMatch needs to be checked against the user_reply
                if kap.keywords.iter().any(|kw| {
                    let kw_rgx = Regex::new(&format!("(?i){}", kw)).unwrap();
                    let captures_vec: Vec<_> = kw_rgx.captures_iter(user_reply.as_str()).collect();
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
                    dbg!("context storage");
                    Some(MatchItem::new(
                        kap.intent_name,
                        kap.grouping,
                        kap.adjacent,
                        start_index,
                        kap.answer_to,
                        // add context storage
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
                    mi_req.intent == mi.intent
                        && req_amount < mi_req.grouping.number
                        && req_id != mi_req.grouping.id
                })
            })
            .collect();

        let regrouped = sufficing_match_items.iter().group_by(|i| i.grouping.id);

        let mut recomposed_match_items: Vec<MatchItem<'a>> = vec![];
        for (_, group) in regrouped.into_iter() {
            let group_vec: Vec<_> = group.collect();
            let count = group_vec.len();

            if count == 1 {
                recomposed_match_items.push(group_vec[0].clone())
            } else {
                let intent_names: Vec<&'a str> = group_vec.iter().map(|g| g.intent).collect();
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
                    // implicit states answering is not taken into acount with composed intents
                    &[],
                    // there will be empty context for composed intents
                );

                recomposed_match_items.push(recomposed_intent)
            }
        }

        // increment implicitly answered states usage
        recomposed_match_items.iter().for_each(|k| {
            k.answer_to.iter().for_each(|at| {
                let new_state_usage = csi.states_usage.entry(at.to_string()).or_insert(0);
                *new_state_usage += 1;
            })
        });

        // add to csi.context - intent is there, replace with new adjacent states

        MatchedStates {
            c_status_in: csi,
            matched_states: recomposed_match_items,
        }
    }
}
