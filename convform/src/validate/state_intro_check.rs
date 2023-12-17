use super::super::Flow;
use super::helper_structs_validate::IssueItem;

impl<'a> Flow<'a> {
    pub fn state_intro_present(&self) -> Vec<IssueItem> {
        if self.states.iter().any(|r| *r.0 == "state_intro") {
            vec![]
        } else {
            vec![IssueItem::MissingStateIntro]
        }
    }
}
