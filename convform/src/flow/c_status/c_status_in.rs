pub mod get_stringmatching_pool;
mod handle_matched_states;
mod initiative;
mod match_states;
mod matched_states;
mod non_initiative;
pub mod response_states;
mod rhematize;
mod stringmatching_pool;
use crate::flow::Flow;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
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

    pub fn view_user_reply(&self) -> &'a str {
        self.user_reply
    }

    pub fn update_usage(&mut self, rs: &[&'a str]) -> HashMap<&'a str, usize> {
        rs.iter().for_each(|rs| {
            let entry = self.states_usage.entry(rs).or_insert(0);
            *entry += 1;
        });
        self.states_usage.clone()
    }
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
