use crate::flow::ResponseType;

use super::super::Flow;
use super::helper_structs_validate::{
    are_same_variant, ConvItem, IssueItem, MissRef, ValidateReferences, ValidationDeclaration,
    ValidationReference,
};

impl<'a> Flow<'a> {
    pub fn validate_used(
        used: &'a [ValidationReference<'a>],
        declared: &[ValidationDeclaration<'a>],
    ) -> Vec<IssueItem<'a>> {
        used.iter()
            .filter(|vr| {
                !declared.iter().any(|dr| {
                    dr.item_name == vr.item_name && are_same_variant(&dr.item_type, &vr.item_type)
                })
            })
            .map(|nonvalid_ref| {
                IssueItem::MissingReference(MissRef {
                    typ: nonvalid_ref.item_type,
                    name: nonvalid_ref.item_name,
                    wher: &nonvalid_ref.origin_name,
                    otyp: nonvalid_ref.origin_type, // in states intents adjacent this field is used to identify intent
                })
            })
            .collect()
    }

    pub fn validate_declared(
        used: &[ValidationReference<'a>],
        declared: &[ValidationDeclaration<'a>],
    ) -> Vec<IssueItem<'a>> {
        declared
            .iter()
            .filter(|dr| {
                !used.iter().any(|vr| {
                    dr.item_name == vr.item_name && are_same_variant(&dr.item_type, &vr.item_type)
                })
            })
            .filter(|unsued| !unsued.allow_unit)
            .map(|nonvalid_ref| {
                IssueItem::UnusedDeclared((nonvalid_ref.item_name, nonvalid_ref.item_type))
            })
            .collect()
    }

    pub fn get_used(&self) -> Vec<ValidationReference<'a>> {
        let track_iter = self.get_refs();
        let states_iter = self.states.values().flat_map(|s| s.get_refs());
        let intents_iter = self.intents.values().flat_map(|s| s.get_refs());
        states_iter.chain(intents_iter).chain(track_iter).collect()
    }

    pub fn get_declared(&self) -> Vec<ValidationDeclaration<'a>> {
        let v = vec![
            self.states
                .iter()
                .map(|s| ValidationDeclaration {
                    item_name: s.0,
                    item_type: ConvItem::State,
                    allow_unit: are_same_variant(&s.1.state_type, &ResponseType::Initiative)
                        || are_same_variant(&s.1.state_type, &ResponseType::Flexible)
                        || are_same_variant(&s.1.state_type, &ResponseType::Solo)
                        || *s.0 == "no input response",
                })
                .collect::<Vec<_>>(),
            self.intents
                .keys()
                .map(|i| ValidationDeclaration {
                    item_name: i,
                    item_type: ConvItem::Intent,
                    allow_unit: false,
                })
                .collect::<Vec<_>>(),
        ]
        .iter()
        .flatten()
        .cloned()
        .collect::<Vec<_>>();
        // println!("{:#?}", v);
        v
    }
}
