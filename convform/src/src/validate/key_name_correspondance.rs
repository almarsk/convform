use super::super::Flow;
use super::helper_structs_validate::{ConvItem, IssueItem, ValidateReferences};

#[derive(Debug)]
pub struct NoncorrespondingItem<'a> {
    pub item_name: &'a str,
    pub item_type: &'a str,
}

impl<'a> Flow<'a> {
    pub fn key_name_correspond(&self) -> Vec<IssueItem> {
        let items: Vec<(&'a str, &'a str, ConvItem)> = vec![
            self.states
                .iter()
                .map(|s| (*s.0, s.1.get_name().0, ConvItem::State))
                .collect::<Vec<_>>(),
            self.intents
                .iter()
                .map(|i| (*i.0, i.1.get_name().0, ConvItem::Intent))
                .collect::<Vec<_>>(),
        ]
        .iter()
        .flatten()
        .cloned()
        .collect();

        items
            .iter()
            .filter(|item| item.0 != item.1)
            .map(|nc| IssueItem::DifferentKeyName((nc.0, nc.1, nc.2)))
            .collect()
    }
}
