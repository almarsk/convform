use super::c_status_in::response_states::ResponseStates;
use super::Flow;
use pyo3::prelude::*;

use rand::{thread_rng, Rng};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

impl<'a> ResponseStates<'a> {
    pub fn create_c_state_out(self, flow: &Flow) -> CStatusOut {
        CStatusOut::new(self, flow)
    }
}

#[derive(Deserialize, Serialize, Debug, Default)]
#[allow(dead_code)]
#[pyclass]
pub struct CStatusOut {
    bot_reply: String,
    routine: String,
    superstate: String,
    last_states: Vec<String>,
    states_usage: HashMap<String, usize>,
    turns_since_initiative: usize,
}

impl<'a> CStatusOut {
    pub fn new(rs: ResponseStates<'a>, flow: &Flow) -> CStatusOut {
        let (rs, mut csi, superstate) = rs.get_fields();
        let states_usage = csi.update_usage(&rs);
        let bot_reply = compose_bot_reply(&rs, flow);

        CStatusOut {
            bot_reply,
            superstate: superstate.to_string(),
            last_states: rs.into_iter().map(|s| s.to_string()).collect(),
            turns_since_initiative: csi.tsi(),
            // might be fallback later
            routine: csi.routine().to_string(),
            states_usage: states_usage
                .into_iter()
                .map(|(s, u)| (s.to_string(), u))
                .collect(),
        }

        // get random say from each response state
        // how to handle fallback and how to communicate it in responsestates?
    }
}

fn compose_bot_reply(rs: &[&str], flow: &Flow) -> String {
    let mut rng = thread_rng();
    rs.iter()
        .map(|rs| {
            if let Some(state) = flow.states.iter().find(|fs| fs.1.state_name == *rs) {
                let says = state.1.say.clone();
                let n = rng.gen_range(0..says.len());
                says[n]
            } else {
                ""
            }
        })
        .fold(String::new(), |acc, x| format!("{} {}", acc, x))
        .trim()
        .to_string()
}
