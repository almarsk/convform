use super::super::validate::helper_structs_validate::are_same_variant;
use super::promptify::promptify;
use super::response_states::ResponseStates;
use super::Flow;
use super::{super::flow::ResponseType, csi::CStatusIn};
use pyo3::prelude::*;
use rand::{thread_rng, Rng};
use serde::Serialize;
use std::collections::HashMap;

#[derive(Debug, Default, Serialize)]
#[allow(dead_code)]
#[pyclass]
pub struct CStatusOut {
    #[pyo3(get, set)]
    pub bot_reply: String, // this has to be assembled
    #[pyo3(get, set)]
    pub last_states: Vec<String>,
    #[pyo3(get, set)]
    pub states_usage: HashMap<String, usize>,
    #[pyo3(get, set)]
    pub turns_since_initiative: usize,
    #[pyo3(get, set)]
    pub bot_turns: usize,
    #[pyo3(get, set)]
    pub prompt: String,
    #[pyo3(get, set)]
    pub coda: bool,
    #[pyo3(get, set)]
    pub initiativity: usize,
    #[pyo3(get, set)]
    pub context: HashMap<String, (Vec<String>, String)>,
    // add context storage
}

impl<'a> CStatusOut {
    pub fn new(rs: ResponseStates<'a>, flow: &Flow) -> CStatusOut {
        let (rs, mut csi) = rs.get_fields();

        let states_usage = csi
            .update_usage(&rs)
            .into_iter()
            .map(|(s, u)| (s.to_string(), u))
            .collect();

        let bot_reply = compose_bot_reply(&rs, flow);
        let last_states: Vec<String> = rs.iter().map(|s| s.to_string()).collect();
        let turns_since_initiative = turns_since_init(flow, &last_states, &csi);

        let coda = csi.coda || last_states.contains(&flow.coda.to_string());
        let initiativity = get_initiativity(flow, &last_states, &mut csi);
        let context = csi.context;

        crate::cnd_dbg!(&last_states);
        crate::cnd_dbg!(&csi.coda);
        crate::cnd_dbg!(&csi.last_states.contains(&flow.coda.to_string()));

        CStatusOut {
            bot_reply,
            last_states,
            turns_since_initiative,
            bot_turns: csi.bot_turns + 1,
            states_usage,
            prompt: String::from(""),
            coda,
            initiativity,
            context,
        }
    }

    pub fn issue(issue: String) -> Self {
        CStatusOut {
            bot_reply: issue,
            ..Default::default()
        }
    }
}

fn compose_bot_reply(rs: &[&str], flow: &Flow) -> String {
    let mut rng = thread_rng();
    let dumb_answer = rs
        .iter()
        .map(|rs| {
            if let Some(state) = flow.states.iter().find(|fs| fs.1.state_name == *rs) {
                let says = state.1.say.clone();
                let n = rng.gen_range(0..says.len());
                let raw_answer = says[n];
                raw_answer.to_string()
            } else {
                "".to_string()
            }
        })
        .fold(String::new(), |acc, x| format!("{} {}", acc, x))
        .trim()
        .to_string();
    promptify(dumb_answer)
}

fn get_initiativity(flow: &Flow, states: &[String], csi: &mut CStatusIn) -> usize {
    let init_vec: Vec<usize> = states
        .iter()
        .filter_map(|s| {
            let init = flow
                .states
                .iter()
                .find(|state| state.0 == s)
                .unwrap()
                .1
                .initiativity;
            if init.is_some() {
                init
            } else {
                None
            }
        })
        .collect();

    if let Some(i) = init_vec.iter().max() {
        // could also be min maybe, up to testing
        *i
    } else {
        csi.initiativity
    }
}

fn turns_since_init(flow: &Flow, last_states: &[String], csi: &CStatusIn) -> usize {
    let last_init: Vec<&String> = last_states
        .iter()
        .filter(|s| {
            let state_type = &flow
                .states
                .values()
                .find(|state| s.as_str() == state.state_name)
                .unwrap()
                .state_type;

            are_same_variant(state_type, &ResponseType::Initiative)
                || are_same_variant(state_type, &ResponseType::Flexible)
                || are_same_variant(state_type, &ResponseType::Solo)
        })
        .collect();
    if last_init.is_empty() {
        csi.turns_since_initiative + 1
    } else {
        0
    }
}
