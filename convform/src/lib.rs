mod flow;
use flow::c_status::c_status;
pub use flow::c_status::CStatusOut;
pub use flow::Flow;
use pyo3::prelude::*;
use std::fs::read_to_string;

#[pymethods]
impl CStatusOut {
    #[new]
    pub fn get_bot_reply(bot_name: &str, csi: PyObject, py: Python) -> CStatusOut {
        let path = format!("convform/bots/{}.json", bot_name);
        let file = read_to_string(path.as_str()).unwrap();

        match Flow::validate_behavior(bot_name, &file) {
            Err(e) => {
                println!("{:?}", e);
                CStatusOut::issue(String::from("ERROR: json validation unsuccesful"))
            }
            Ok(flow) => {
                //let path_csi = format!("bots/csi/{}.json", csi);
                //let csi = read_to_string(path_csi.as_str()).unwrap();
                match c_status(csi, &flow, py) {
                    Ok(cso) => cso,
                    Err(e) => {
                        println!("{:?}", e);
                        CStatusOut::issue(String::from("ERROR: issue making cso"))
                    }
                }
            }
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
