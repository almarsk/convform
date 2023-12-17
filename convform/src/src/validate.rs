use super::Flow;
mod empty_fields;
pub mod helper_structs_validate;
use helper_structs_validate::IssueItem;
mod key_name_correspondance;
mod placeholders;
mod state_intro_check;
pub mod validate_refs;
use self::autoserialize::autoserialize;
pub mod autoserialize;
mod prompt;
mod silence;
mod space;
mod trait_edit;
mod validate_regex;

impl<'a> Flow<'a> {
    pub fn validate_behavior(path: &str, file: &'a str) -> Result<Flow<'a>, String> {
        let flow = Self::parse_into_flow(file)?;

        let used = flow.get_used();
        let declared = flow.get_declared();
        let edit_checks = [
            Flow::validate_used(&used, &declared),
            Flow::validate_declared(&used, &declared),
            flow.silence(),
        ];

        let edit_issues: Vec<&IssueItem<'_>> = edit_checks
            .iter()
            .filter(|c| !c.is_empty())
            .flatten()
            .collect();
        if !edit_issues.is_empty() {
            println!("{:?}", autoserialize(&flow, path, edit_issues));
        }

        let checks = [
            Flow::validate_used(&used, &declared),
            flow.check_for_empty(),
            flow.validate_regex(),
            flow.key_name_correspond(),
            flow.state_intro_present(),
            flow.placeholder_in_state(),
            flow.placeholder_in_intent(),
            flow.prompt(),
            flow.check_for_space(),
        ];

        let issues: Vec<&IssueItem<'_>> =
            checks.iter().filter(|c| !c.is_empty()).flatten().collect();

        if issues.is_empty() {
            Ok(flow)
        } else {
            Err(issues.iter().fold(String::new(), |mut summary, issue| {
                summary.push_str(issue.format_issues().as_str());
                summary
            }))
        }
    }

    fn parse_into_flow(file: &'a str) -> Result<Flow<'a>, String> {
        match serde_json::from_str(file) {
            Ok(chatbot_instructions) => Ok(chatbot_instructions),
            Err(e) => Err(format!("Issue parsing json, {:?}", e)),
        }
    }
}
