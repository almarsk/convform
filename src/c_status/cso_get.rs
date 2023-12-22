use super::response_states::ResponseStates;
use super::CStatusOut;
use super::Flow;

impl<'a> ResponseStates<'a> {
    pub fn create_cso(self, flow: &Flow) -> CStatusOut {
        CStatusOut::new(self, flow)
    }
}
