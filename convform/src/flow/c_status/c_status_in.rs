use serde_json::Value;
use std::collections::HashMap;
mod initiative;
mod non_initiative;
mod rhematize;
use crate::flow::Flow;
use serde::{Deserialize, Serialize};
mod matched_states;
pub mod response_states;
mod stringmatching_pool;
use stringmatching_pool::StringMatchingPool;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct CStatusIn<'a> {
    routine: &'a str,
    superstate: &'a str,
    user_reply: &'a str,
    last_states: Vec<&'a str>,
    states_usage: HashMap<&'a str, usize>,
    turns_since_initiative: usize,
}

impl<'a> CStatusIn<'a> {
    pub fn parse_into_c_status_in(file: &'a str) -> Result<CStatusIn, String> {
        match serde_json::from_str::<CStatusIn>(file) {
            Ok(c_status_in) => {
                //println!("\nuser said: {}\n", c_status_in.user_reply);
                Ok(c_status_in)
            }
            Err(e) => Err(format!("Issue parsing json, {:?}", e)),
        }
    }

    pub fn treat(self, flow: &'a Flow) -> Self {
        let mut treated_csi = self;

        if treated_csi.routine.is_empty() {
            treated_csi.routine = flow.routines.first_key_value().unwrap().1.routine_name;
        };

        if treated_csi.superstate.is_empty() {
            treated_csi.superstate = flow
                .routines
                .iter()
                .find(|s| s.1.routine_name == treated_csi.routine)
                .unwrap()
                .1
                .order_superstates[0]
        };

        treated_csi
    }

    pub fn tsi(&self) -> usize {
        self.turns_since_initiative
    }

    pub fn routine(&self) -> &'a str {
        self.routine
    }

    pub fn update_usage(&mut self, rs: &[&'a str]) -> HashMap<&'a str, usize> {
        //println!("{:?}", self.states_usage);
        rs.iter().for_each(|rs| {
            println!(
                "state {} usage {}",
                rs,
                self.states_usage.get(rs).unwrap_or(&0usize)
            );
            match self.states_usage.get(rs) {
                Some(i) => self.states_usage.insert(rs, i + 1),
                None => self.states_usage.insert(rs, 1),
            };
        });
        self.states_usage.clone()
    }

    pub fn get_string_matching_pool(self, flow: &'a Flow<'a>) -> StringMatchingPool<'a> {
        let mut kap_last_states =
            CStatusIn::extract_kaps_from_vec_of_states(&self.last_states, flow);

        // take current superstate, get all the states from it and filter by the ones which have superstate global on true
        // the filter those to only have superstates which arent in the csi.last_states
        // extract_kaps from the resulting vec
        let current_superstate_name = self.superstate;
        let current_superstate_full = flow
            .superstates
            .iter()
            .find(|s| s.0 == &current_superstate_name)
            .unwrap()
            .1;
        let current_states_global_not_in_last: Vec<&str> = current_superstate_full
            .states
            .iter()
            .filter(|s| {
                let state = flow.states.iter().find(|ps| &ps.0 == s).unwrap().1;
                state.superstate_global
            })
            .filter(|s| !self.last_states.contains(s))
            .copied()
            .collect();

        if !current_states_global_not_in_last.is_empty() {
            kap_last_states.extend(CStatusIn::extract_kaps_from_vec_of_states(
                &current_states_global_not_in_last,
                flow,
            ))
        }

        StringMatchingPool::new(self, kap_last_states)
    }

    pub fn view_user_reply(&self) -> &'a str {
        self.user_reply
    }

    fn extract_kaps_from_vec_of_states(states: &[&'a str], flow: &'a Flow<'a>) -> Vec<ToMatch<'a>> {
        states
            .iter()
            .filter_map(|ls| {
                flow.states
                    .values()
                    .find(|state| &state.state_name == ls)
                    .map(|l_state| {
                        l_state
                            .intents
                            .iter()
                            .map(|intent_on_state| {
                                let current_intent_set: Vec<&'a str> =
                                    intent_on_state.0.split('+').map(|i| i.trim()).collect();

                                let current_keywords_set: HashMap<&'a str, Vec<&'a str>> =
                                    current_intent_set
                                        .iter()
                                        .map(|subintent| {
                                            (*intent_on_state.0, get_keywords(flow, subintent))
                                        })
                                        .collect();
                                let current_answer_to_set: Vec<&'a str> = current_intent_set
                                    .iter()
                                    .flat_map(|subintent| get_answer_to(flow, subintent))
                                    .collect();

                                let mut current_adjacent: Vec<_> = vec![];

                                if let Some(f_intent) = flow
                                    .intents
                                    .iter()
                                    .find(|(_, i)| *intent_on_state.0 == i.intent_name)
                                {
                                    let adjacent: Vec<_> =
                                        intent_on_state // this will extend mutable adjacent
                                            .1
                                            .iter()
                                            .chain(f_intent.1.adjacent.iter())
                                            .cloned()
                                            .filter(|a| a != &"$")
                                            .collect();
                                    current_adjacent = adjacent;
                                };

                                let tm = ToMatch::new(
                                    current_keywords_set,
                                    current_adjacent,
                                    current_answer_to_set,
                                );
                                //println!("{:?}", tm);
                                tm
                            })
                            .collect::<Vec<_>>()
                    })
            })
            .flatten()
            .collect()
    }
}

#[derive(Debug)]
pub struct ToMatch<'a> {
    keywords: HashMap<&'a str, Vec<&'a str>>,
    adjacent: Vec<&'a str>,
    answer_to: Vec<&'a str>,
}

impl<'a> ToMatch<'a> {
    pub fn new(
        keywords: HashMap<&'a str, Vec<&'a str>>,
        adjacent: Vec<&'a str>,
        answer_to: Vec<&'a str>,
    ) -> Self {
        ToMatch {
            keywords,
            adjacent,
            answer_to,
        }
    }
}

fn get_keywords<'a>(flow: &'a Flow, intent: &str) -> Vec<&'a str> {
    flow.intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| f_intent.1.keywords.clone())
        .unwrap()
}

fn get_answer_to<'a>(flow: &'a Flow, intent: &str) -> Vec<&'a str> {
    flow.intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| f_intent.1.answer_to.clone())
        .unwrap()
}

pub trait FromValue<'a> {
    fn from_value(value: &'a Value) -> Result<Self, String>
    where
        Self: Sized;
}

impl<'a> FromValue<'a> for CStatusIn<'a> {
    fn from_value(value: &'a Value) -> Result<Self, String> {
        let routine = value["routine"].as_str().ok_or("Missing or invalid routine")?;
        let superstate = value["superstate"].as_str().ok_or("Missing or invalid superstate")?;
        let user_reply = value["user_reply"].as_str().ok_or("Missing or invalid user reply")?;
        let last_states = value["last_states"]
            .as_array()
            .unwrap_or_else(|| panic!("Expected an array"))
            .iter()
            .map(|v| v.as_str().unwrap_or(""))
            .collect();

        let mut states_usage = HashMap::new();
        if let Some(obj) = value["states_usage"].as_object() {
            for (key, value) in obj {
                if let Some(value_as_u64) = value.as_u64() {
                    states_usage.insert(key.as_str(), value_as_u64 as usize);
                }
            }
        }

        let turns_since_initiative = value["turns_since_initiative"]
            .as_u64()
            .ok_or("Issue parsing turns since initiative")?
            as usize;

        Ok(CStatusIn {
            routine,
            superstate,
            user_reply,
            last_states,
            states_usage,
            turns_since_initiative,
        })
    }
}
