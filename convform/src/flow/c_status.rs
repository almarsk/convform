use super::Flow;
use c_status_in::FromValue;
use pyo3::prelude::*;
use serde_json::Value;
pub mod c_status_in;
mod c_status_out;
use c_status_in::CStatusIn;
pub use c_status_out::CStatusOut;

#[allow(dead_code)]
pub fn c_status(input: String, flow: &Flow, _py: Python) -> Result<CStatusOut, String> {
    let parsed_json: Value = serde_json::from_str(input.as_str()).map_err(|e| e.to_string())?;
    let csi: CStatusIn = CStatusIn::from_value(&parsed_json)?; // not great - could be made from_str

    // println!("{:#?}", csi);

    Ok(csi
        .treat(flow)
        .get_stringmatching_pool(flow)
        .match_states()
        .handle_matched_states(flow)
        .create_c_state_out(flow))
}
