use super::{helper_structs_validate::IssueItem, Flow};

impl<'a> Flow<'a> {
    pub fn check_for_space(&self) -> Vec<IssueItem> {
        self.states
            .iter()
            .flat_map(|s| {
                s.1.intents.iter().filter_map(|i| {
                    if i.0.contains(" +")
                        || i.0.contains("+ ")
                        || i.0.starts_with(' ')
                        || i.0.ends_with(' ')
                    {
                        Some(IssueItem::ExtraSpace((s.0, i.0)))
                    } else {
                        None
                    }
                })
            })
            .collect()
    }
}
