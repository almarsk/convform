mod flow;
use flow::c_status::c_status;
use flow::c_status::c_status_out::CStatusOut;
pub use flow::Flow;
use pyo3::prelude::*;
use pyo3::Python;

use std::fs::read_to_string;

#[pymethods]
impl CStatusOut {
    #[allow(unused_must_use)]
    #[new]
    pub fn get_bot_reply(path: &str, bot_name: &str, csi: PyObject, py: Python) -> Self {
        println!("q{:?}", csi);
        let path = format!("{}/{}.json", path, bot_name);
        let file = read_to_string(path.as_str()).unwrap();

        match Flow::validate_behavior(bot_name, &file) {
            Err(e) => {
                println!("v{e}\n");
                CStatusOut::default()
            }
            Ok(flow) => {
                // let path_csi = format!("convform_/bots/csi/{}.json", csi);
                // println!("{}", path_csi);
                // let csi = read_to_string(path_csi.as_str()).unwrap();
                let cso = c_status(csi, &flow, py);
                match cso {
                    Ok(o) => o,
                    Err(e) => {
                        println!("c{e}\n");
                        CStatusOut::default()
                    }
                }
            }
        }
    }

    pub fn show(&self) -> &Self {
        self
    }
}

#[pymodule]
fn convform(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<CStatusOut>()?;
    Ok(())
}
