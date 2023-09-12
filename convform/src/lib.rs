mod flow;
use flow::c_status::{c_status, CStatusOut};
pub use flow::Flow;
use pyo3::prelude::*;
use std::fs::read_to_string;

#[pymethods]
impl CStatusOut {
    #[new]
    pub fn get_bot_reply(bot_name: &str, csi: String, py: Python) -> CStatusOut {
        let path = format!("convform/bots/{}.json", bot_name);
        let file = read_to_string(path.as_str()).unwrap();

        match Flow::validate_behavior(path.as_str(), &file) {
            Err(e) => {
                println!("validation error: {:?}", e);
                CStatusOut::issue(String::from("ERROR: json validation unsuccesful"))
                // not great - better make PyResult
            }
            Ok(flow) => match c_status(csi, &flow, py) {
                Ok(cso) => cso,
                Err(e) => {
                    println!("cstatus_out error: {:?}", e);
                    CStatusOut::issue(String::from("ERROR: issue making cso")) // not great - better make PyResult
                }
            },
        }
    }
    pub fn show(&self) {
        println!("{:#?}", self)
    }
}

#[pymodule]
fn convform(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<CStatusOut>()?;
    Ok(())
}
