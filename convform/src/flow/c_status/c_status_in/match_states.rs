use super::matched_states::MatchedStates;
use super::StringMatchingPool;
use regex::Regex;

#[derive(Clone, Debug)]
pub struct MatchItem<'a> {
    _intent: &'a str,
    states: Vec<&'a str>,
    index_start: usize,
}

impl<'a> MatchItem<'a> {
    fn new(_intent: &'a str, states: Vec<&'a str>, index_start: usize) -> Self {
        MatchItem {
            _intent,
            states,
            index_start,
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
    pub fn match_states(self) -> MatchedStates<'a> {
        let mut csi = self.get_csi();
        let user_reply = csi.view_user_reply();
        let kaps = self.get_kaps();

        // check if beginning of conversation - return state intro
        if csi.view_user_reply().is_empty() {
            // beginning of conversation
            return MatchedStates::new(csi, vec![MatchItem::new("", vec!["state_intro"], 0)]);
        } else {
            // increment implicitly answered states usage
            kaps.iter().for_each(|k| {
                k.answer_to().iter().for_each(|at| {
                    let new_state_usage = csi.states_usage.entry(*at).or_insert(0);
                    *new_state_usage += 1;
                })
            });

            // each ToMatch in kaps needs to be check against the user_reply
            let match_items: Vec<MatchItem<'a>> = kaps
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
                        Some(MatchItem::new(kap.intent_name, kap.adjacent, start_index))
                    } else {
                        None
                    }
                })
                .collect::<Vec<MatchItem<'a>>>();

            println!("{:#?}", match_items);

            MatchedStates::new(csi, match_items)
        }
    }

    // answerto will be used to modify csi state usage history
}
