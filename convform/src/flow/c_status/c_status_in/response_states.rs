use super::CStatusIn;

#[derive(Debug)]
pub struct ResponseStates<'a> {
    response_states: Vec<&'a str>,
    c_status_in: CStatusIn<'a>,
    superstate: &'a str,
}

impl<'a> ResponseStates<'a> {
    pub fn new(
        response_states: Vec<&'a str>,
        c_status_in: CStatusIn<'a>,
        superstate: Option<&'a str>,
    ) -> ResponseStates<'a> {
        // THERE WILL BE FALLBACK INFORMATION
        // WHICH WILL CHANGE BEHAVIOR
        // IN CASE OF EMPTY RESPONSE STATES VEC

        let current_superstate = if let Some(s) = superstate {
            s
        } else {
            c_status_in.superstate
        };

        ResponseStates {
            response_states,
            c_status_in,
            superstate: current_superstate,
        }
    }
    pub fn get_fields(self) -> (Vec<&'a str>, CStatusIn<'a>, &'a str) {
        (self.response_states, self.c_status_in, self.superstate)
    }
}
