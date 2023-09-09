use super::trait_edit::Edit;
use super::{super::Flow, helper_structs_validate::IssueItem};
use std::fs::File;

#[derive(Debug)]
pub enum Edited {
    ChangesMade,
    NoChangesMade,
}

pub fn autoserialize(
    flow: &Flow,
    path: &str,
    issues: Vec<&IssueItem>,
) -> Result<Edited, std::io::Error> {
    let mut edited_flow = flow.clone();

    if !issues.is_empty() {
        edit_flow(&mut edited_flow, issues);
        if let Err(e) = serialize_edited(&edited_flow, path) {
            Err(e)
        } else {
            Ok(Edited::ChangesMade)
        }
    } else {
        Ok(Edited::NoChangesMade)
    }
}

// make a copy of Flow, delete declared, add templates of missing
// serialize into {name_of_bot}_auto.json
//

fn edit_flow<'a>(flow: &mut Flow<'a>, items: Vec<&IssueItem<'a>>) {
    // remove/add empty template structs
    for item in items {
        flow.edit(item)
    }
}

fn serialize_edited(edited: &Flow, path: &str) -> Result<(), std::io::Error> {
    let serialized = serde_json::to_string(edited)?;
    let path = format!("{}_edited.json", path.trim_end_matches(".json"));
    println!("{path}");
    File::create(&path)?;

    std::fs::write(path, serialized)
}
