use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
pub mod c_status;
mod validate;
pub use validate::autoserialize;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct Flow<'a> {
    persona: &'a str,
    routines: BTreeMap<&'a str, Routine<'a>>,
    superstates: BTreeMap<&'a str, Superstate<'a>>,
    states: BTreeMap<&'a str, State<'a>>,
    intents: BTreeMap<&'a str, Intent<'a>>,
}

#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub enum ResponseType {
    Responsive,
    Initiative,
    #[default]
    Flexible,
    Solo,
    Connective,
    Priority,
}

#[derive(Deserialize, Serialize, Debug, Clone)]
struct Routine<'a> {
    routine_name: &'a str,
    max_says_at_once: usize,
    the_track: &'a str,
    order_superstates: Vec<&'a str>,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default)]
struct Superstate<'a> {
    superstate_name: &'a str,
    #[serde(default = "default_usize")]
    initiativeness: usize,
    states: Vec<&'a str>,
    description: &'a str,
}

pub fn default_usize() -> usize {
    2
}

#[derive(Serialize, Deserialize, Debug, Clone, Default)]
struct State<'a> {
    state_name: &'a str,
    intents: BTreeMap<&'a str, Vec<&'a str>>,
    say_annotation: &'a str,
    say: Vec<&'a str>,
    over_iterated_say: Vec<&'a str>,
    state_type: ResponseType,
    #[serde(default = "default_iteration")]
    iteration: usize,
    #[serde(default = "default_bool")]
    superstate_global: bool,
    #[serde(default = "default_bool")]
    prioritize: bool,
}

pub fn default_iteration() -> usize {
    1
}
pub fn default_bool() -> bool {
    false
}

#[derive(Serialize, Deserialize, Debug, Clone, Default)]
struct Intent<'a> {
    intent_name: &'a str,
    intent_annotation: &'a str,
    keywords: Vec<&'a str>,
    adjacent: Vec<&'a str>,
    #[serde(default = "default_vec")]
    answer_to: Vec<&'a str>,
}

pub fn default_vec<'a>() -> Vec<&'a str> {
    vec![]
}
