use super::super::Flow;
use super::helper_structs_validate::IssueItem;

impl<'a> Flow<'a> {
    pub fn state_intro_present(&self) -> Vec<IssueItem> {
        if let Some(routine) = self.routines.iter().find(|r| *r.0 == "standard") {
            if let Some(superstate_name) = routine.1.order_superstates.first() {
                if let Some(found_superstate) = self
                    .superstates
                    .iter()
                    .find(|superstate| &superstate.1.superstate_name == superstate_name)
                {
                    if !found_superstate.1.states.contains(&"state_intro") {
                        vec![IssueItem::MissingStateIntro((
                            routine.1.routine_name,
                            found_superstate.1.superstate_name,
                        ))]
                    } else {
                        vec![]
                    }
                } else {
                    vec![]
                }
            } else {
                vec![]
            }
        } else {
            vec![IssueItem::MissingStateIntro(("standard", "missing"))]
        }
    }
}
