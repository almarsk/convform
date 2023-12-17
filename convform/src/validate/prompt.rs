use super::Flow;
use super::IssueItem;

impl<'a> Flow<'a> {
    pub fn prompt(&self) -> Vec<IssueItem> {
        self.states
            .iter()
            .filter_map(|state| {
                let invalid_prompts: Vec<IssueItem> = state
                    .1
                    .say
                    .iter()
                    .filter_map(|say| {
                        if !valid_prompting(say) {
                            Some(IssueItem::InvalidPrompt((state.0, say)))
                        } else {
                            None
                        }
                    })
                    .collect();
                if invalid_prompts.is_empty() {
                    None
                } else {
                    Some(invalid_prompts)
                }
            })
            .flatten()
            .collect()
    }
}

fn valid_prompting(say: &str) -> bool {
    !say.contains("###") || say.contains("###") && say.starts_with("###") && say.ends_with("###")
}
