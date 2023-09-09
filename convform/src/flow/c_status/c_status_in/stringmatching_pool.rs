use super::matched_states::{MatchItem, MatchedStates};
use super::CStatusIn;
use super::ToMatch;
use regex::Regex;

#[derive(Clone)]
pub struct StringMatchingPool<'a> {
    keywords_adjacent_pairs: Vec<ToMatch<'a>>,
    c_status_in: CStatusIn<'a>,
}

impl<'a> StringMatchingPool<'a> {
    pub fn new(csi: CStatusIn<'a>, kap: Vec<ToMatch<'a>>) -> StringMatchingPool<'a> {
        StringMatchingPool {
            keywords_adjacent_pairs: kap,
            c_status_in: csi,
        }
    }

    pub fn get_kaps(self) -> Vec<ToMatch<'a>> {
        self.keywords_adjacent_pairs
    }

    pub fn get_csi(&self) -> CStatusIn<'a> {
        self.c_status_in.clone()
    }

    pub fn match_states(self) -> MatchedStates<'a> {
        let mut csi = self.get_csi();

        // check if beginning of conversation - return state intro
        if csi.view_user_reply().is_empty() {
            return MatchedStates::new(csi, vec![MatchItem::new(vec![""], vec!["state_intro"], 0)]);
        }

        let mut answered_states: Vec<&'a str> = vec![];
        // println!("kaps: {:#?}", self.clone().get_kaps());
        let ms: Vec<MatchItem<'a>> = self
            .get_kaps()
            .iter()
            .flat_map(|mi| {
                mi.keywords
                    .iter()
                    .filter_map(|kws| {
                        let mut start_indexes: Vec<usize> = Vec::with_capacity(kws.1.len());
                        let mut matched_intents: Vec<&'a str> = vec![];

                        kws.1.iter().for_each(|kw| {
                            let kw_rgx = Regex::new(&format!("(?i){}", kw)).unwrap();
                            let captures = kw_rgx.captures_iter(csi.view_user_reply());
                            let mut start_index = usize::MAX;
                            for cap in captures {
                                println!("Matched sector: {}", cap.get(0).unwrap().as_str());
                                let current_start_index = cap.get(0).unwrap().start();
                                if start_index > current_start_index {
                                    start_index = current_start_index
                                }
                            }
                            start_indexes.push(start_index);
                            if !matched_intents.contains(kws.0) {
                                matched_intents.push(kws.0)
                            }
                        });
                        //println!("start indexes for {:?} {:?}", kws, start_indexes);
                        if start_indexes.iter().all(|si| *si == usize::MAX) {
                            None
                        } else {
                            let matched_start_indexes: Vec<usize> = start_indexes
                                .iter()
                                .filter(|si| *si != &usize::MAX)
                                .copied()
                                .collect();

                            answered_states.extend(mi.answer_to.clone());
                            println!("matched_intent: {:?}", matched_intents);
                            Some(MatchItem::new(
                                matched_intents,
                                mi.adjacent.clone(),
                                matched_start_indexes[matched_start_indexes.len() - 1],
                            ))
                        }
                    })
                    .collect::<Vec<_>>()
            })
            .collect();

        answered_states.iter().for_each(|answered_state| {
            let state_in_history = csi.states_usage.get(answered_state).copied();
            let new_state_usage = if let Some(i) = state_in_history {
                i + 1
            } else {
                1
            };
            csi.states_usage.insert(answered_state, new_state_usage);
        });

        // println!("{:#?}", csi.states_usage);
        // println!("\n\nmatched: {:#?}\n\n", ms);
        MatchedStates::new(csi, ms)
    }
}
