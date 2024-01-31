use crate::flow::Flow;

use super::CStatusIn;

#[derive(Debug)]
pub struct ResponseStates<'a> {
    response_states: Vec<&'a str>,
    c_status_in: CStatusIn,
    prompt: Option<String>,
}

impl<'a> ResponseStates<'a> {
    pub fn new(
        response_states: Vec<&'a str>,
        c_status_in: CStatusIn,
        flow: &'a Flow,
    ) -> ResponseStates<'a> {
        let prompt = if !response_states.is_empty() || c_status_in.coda {
            None
        } else {
            crate::cnd_dbg!("TODO empty response states prompt here");
            Some(flow.persona.to_string())
        };

        ResponseStates {
            response_states,
            c_status_in,
            prompt,
        }
    }
    pub fn get_fields(self) -> (Vec<&'a str>, CStatusIn, Option<String>) {
        (self.response_states, self.c_status_in, self.prompt)
    }
}
