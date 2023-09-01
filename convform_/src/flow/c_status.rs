use super::Flow;
pub mod c_status_in;
pub mod c_status_out;
use crate::flow::c_status::c_status_in::CStatusIn;
use c_status_out::CStatusOut;
use pyo3::PyErr;

use pyo3::PyObject;
use pyo3::Python;

pub fn c_status<'a>(csi: PyObject, flow: &'a Flow, py: Python) -> Result<CStatusOut, PyErr> {
    let cstatus_in: CStatusIn = csi.extract(py)?;

    Ok(cstatus_in
        .treat(flow)
        .get_string_matching_pool(flow)
        .match_states()
        .handle_matched_states(flow)
        .create_c_state_out(flow))
}
