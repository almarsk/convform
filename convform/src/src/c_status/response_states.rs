use super::CStatusIn;

#[derive(Debug)]
pub struct ResponseStates<'a> {
    response_states: Vec<&'a str>,
    c_status_in: CStatusIn,
}

impl<'a> ResponseStates<'a> {
    pub fn new(response_states: Vec<&'a str>, c_status_in: CStatusIn) -> ResponseStates<'a> {
        // THERE WILL BE FALLBACK INFORMATION
        // WHICH WILL CHANGE BEHAVIOR
        // IN CASE OF EMPTY RESPONSE STATES VEC
        crate::cnd_dbg!("empty response states case needs handling");

        ResponseStates {
            response_states,
            c_status_in,
        }
    }
    pub fn get_fields(self) -> (Vec<&'a str>, CStatusIn) {
        (self.response_states, self.c_status_in)
    }
}
