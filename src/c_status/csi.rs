use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Deserialize, Serialize, Debug, Clone, Default)]
pub struct CStatusIn {
    pub user_reply: String,
    pub last_states: Vec<String>,
    pub states_usage: HashMap<String, usize>,
    pub turns_since_initiative: usize,
    pub bot_turns: usize,
    pub coda: bool,
    pub initiativity: usize,
    pub context: HashMap<String, (Vec<String>, String)>,
}

impl<'a> CStatusIn {
    pub fn update_usage(&mut self, rs: &[&'a str]) -> HashMap<String, usize> {
        rs.iter().for_each(|rs| {
            let entry = self.states_usage.entry(rs.to_string()).or_insert(0);
            *entry += 1;
        });
        self.states_usage.clone()
    }
}
