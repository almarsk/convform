use super::Flow;
pub mod c_status_in;
pub mod c_status_out;
use c_status_in::CStatusIn;
use c_status_out::CStatusOut;

pub fn c_status<'a>(file: &'a str, flow: &'a Flow) -> Result<CStatusOut, String> {
    Ok(CStatusIn::parse_into_c_status_in(file)?
        .get_string_matching_pool(flow)
        .match_states()
        .handle_matched_states(flow)
        .create_c_state_out(flow))
}
