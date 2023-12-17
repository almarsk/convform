mod c_status;
mod cnd_dbg;
use c_status::c_status_pipe;
use c_status::cso::CStatusOut;
mod flow;
use flow::Flow;
use pyo3::prelude::*;
use std::fs::read_to_string;
mod validate;

#[pymethods]
impl CStatusOut {
    #[new]
    pub fn get_bot_reply(bot_name: &str, c_status: String, py: Python, path: &str) -> CStatusOut {
        let path = format!("{}{}.json", path, bot_name);
        let file = read_to_string(path.as_str()).unwrap();

        cnd_dbg!(&path);

        match Flow::validate_behavior(path.as_str(), &file) {
            Err(_e) => {
                crate::cnd_dbg!(&_e);
                CStatusOut::issue(format!("ERROR: json validation unsuccesful, {}", path))
            }
            Ok(flow) => match c_status_pipe(c_status, &flow, py) {
                Ok(cso) => cso,
                Err(_e) => {
                    crate::cnd_dbg!(&_e);
                    CStatusOut::issue(String::from("ERROR: issue making cso"))
                }
            },
        }
    }
    pub fn show(&self) {
        crate::cnd_dbg!(&self);
    }
    pub fn is_reply(&self) -> bool {
        crate::cnd_dbg!(!self.bot_reply.is_empty());
        !self.bot_reply.is_empty()
    }

    pub fn persona(&self, path: &str, bot_name: &str) -> String {
        let path = format!("{}{}.json", path, bot_name);
        let file = read_to_string(path.as_str()).unwrap();
        match Flow::validate_behavior(path.as_str(), &file) {
            Ok(flow) => flow.persona.to_string(),
            _ => "".to_string(),
        }
    }
}

#[pymodule]
fn convform(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<CStatusOut>()?;
    Ok(())
}
