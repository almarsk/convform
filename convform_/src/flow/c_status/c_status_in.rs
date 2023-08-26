mod initiative;
mod non_initiative;
mod rhematize;
use crate::Flow;
use serde::{Deserialize, Serialize};
mod matched_states;
pub mod response_states;
mod stringmatching_pool;
use pyo3::prelude::*;
use std::collections::HashMap;
use stringmatching_pool::StringMatchingPool;

#[derive(Deserialize, Serialize, Debug, Clone, FromPyObject)]
pub struct CStatusIn<'a> {
    routine: &'a str,
    superstate: &'a str,
    user_reply: &'a str,
    last_states: Vec<&'a str>,
    states_usage: HashMap<&'a str, usize>,
    turns_since_initiative: usize,
}

impl<'a> CStatusIn<'a> {
    pub fn parse_into_c_status_in(file: &'a str) -> Result<CStatusIn<'a>, String> {
        match serde_json::from_str::<CStatusIn<'a>>(file) {
            Ok(c_status_in) => {
                println!("\nuser said: {}\n", c_status_in.user_reply);
                Ok(c_status_in)
            }
            Err(e) => Err(format!("Issue parsing json, {:?}", e)),
        }
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
            match self.states_usage.get(rs) {
                Some(i) => self.states_usage.insert(rs, i + 1),
                None => self.states_usage.insert(rs, 1),
            };
        });
        self.states_usage.clone()
    }

    pub fn get_string_matching_pool(self, flow: &'a Flow<'a>) -> StringMatchingPool<'a> {
        let kap = self
            .last_states
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

                                let current_keywords_set: Vec<Vec<&'a str>> = current_intent_set
                                    .iter()
                                    .map(|subintent| get_keywords(flow, subintent))
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
                                // double intent not yet implemented
                                let tm = ToMatch::new(
                                    current_keywords_set,
                                    current_adjacent,
                                    current_answer_to_set,
                                );
                                tm
                            })
                            .collect::<Vec<_>>()
                    })
            })
            .flatten()
            .collect();

        //println!("\nc_status_in.rs 90 debug\nToMatch: {:#?}", kap);
        StringMatchingPool::new(self, kap)
    }

    pub fn view_user_reply(&self) -> &'a str {
        self.user_reply
    }
}

#[derive(Debug)]
pub struct ToMatch<'a> {
    keywords: Vec<Vec<&'a str>>,
    adjacent: Vec<&'a str>,
    answer_to: Vec<&'a str>,
}

impl<'a> ToMatch<'a> {
    pub fn new(
        keywords: Vec<Vec<&'a str>>,
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
