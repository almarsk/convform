use super::Flow;
use pyo3::prelude::*;
pub mod c_status_in;
mod c_status_out;
use c_status_in::CStatusIn;
pub use c_status_out::CStatusOut;

#[allow(dead_code)]
pub fn c_status(input: PyObject, flow: &Flow, py: Python) -> Result<CStatusOut, PyErr> {
    let csi: CStatusIn = input.extract(py)?;

    Ok(csi
        .treat(flow)
        .get_string_matching_pool(flow)
        .match_states()
        .handle_matched_states(flow)
        .create_c_state_out(flow))
}
