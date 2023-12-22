use super::super::Flow;
use super::helper_structs_validate::{FRgx, IssueItem};
use regex::Regex;

impl<'a> Flow<'a> {
    pub fn validate_regex(&self) -> Vec<IssueItem> {
        self.intents
            .iter()
            .flat_map(|i| {
                i.1.keywords.iter().filter_map(|kw| match Regex::new(kw) {
                    Ok(_) => None,
                    Err(err) => Some(IssueItem::FaultyRegex(FRgx {
                        kw,
                        wher: i.1.intent_name,
                        err,
                    })),
                })
            })
            .collect()
    }
}
