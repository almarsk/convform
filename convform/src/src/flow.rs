use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
mod default;
use default::*;
pub mod the_track;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct Flow<'a> {
    pub persona: &'a str,
    pub the_track: Vec<&'a str>,
    pub coda: &'a str,
    pub states: BTreeMap<&'a str, State<'a>>,
    pub intents: BTreeMap<&'a str, Intent<'a>>,
}

#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub enum ResponseType {
    Responsive,
    Initiative,
    #[default]
    Flexible,
    Solo,
    Connective,
}

#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub struct State<'a> {
    pub state_name: &'a str,
    pub intents: BTreeMap<&'a str, Vec<&'a str>>,
    pub say_annotation: &'a str,
    pub say: Vec<&'a str>,
    pub over_iterated_say: Vec<&'a str>,
    pub state_type: ResponseType,
    #[serde(default = "default_iteration")]
    pub iteration: usize,
    #[serde(default = "default_bool")]
    pub prioritize: bool,
    #[serde(default = "default_option_usize")]
    pub initiativity: Option<usize>,
}

#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub struct Intent<'a> {
    pub intent_name: &'a str,
    pub intent_annotation: &'a str,
    pub keywords: Vec<String>,
    pub adjacent: Vec<&'a str>,
    #[serde(default = "default_vec")]
    pub answer_to: Vec<&'a str>,
    #[serde(default = "default_btree")]
    pub context_intents: BTreeMap<&'a str, Vec<&'a str>>,
    // experiment and find out why this was useful in the first place :DD
}
