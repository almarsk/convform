use super::Flow;
use csi::CStatusIn;
use cso::CStatusOut;
use pyo3::prelude::*;

pub mod csi;
pub mod cso;
mod cso_get;
mod initiative;
mod matched_states;
mod matched_states_get;
mod non_initiative;
mod promptify;
mod response_states;
mod response_states_get;
mod stringmatching_pool;
mod stringmatching_pool_get;

pub fn c_status_pipe(input: String, flow: &Flow, _py: Python) -> Result<CStatusOut, String> {
    let csi: CStatusIn = serde_json::from_str(input.as_str()).map_err(|e| e.to_string())?;

    crate::cnd_dbg!(&csi);

    Ok(csi
        .get_stringmatching_pool(flow)
        .get_matched_states(flow)
        .get_response_states(flow)
        .create_cso(flow))
}
