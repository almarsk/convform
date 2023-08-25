use super::helper_structs_validate::{are_same_variant, ConvItem, IssueItem};
use crate::flow::{Flow, Intent, ResponseType, Routine, State, Superstate};
use std::collections::BTreeMap;

impl<'a> Flow<'a> {
    pub fn check_for_empty(&'a self) -> Vec<IssueItem> {
        let routines: Vec<IssueItem> = Self::btree_to_vec(&self.routines);
        let superstates: Vec<IssueItem> = Self::btree_to_vec(&self.superstates);
        let states: Vec<IssueItem> = Self::btree_to_vec(&self.states);
        let intents: Vec<IssueItem> = Self::btree_to_vec(&self.intents);
        let flow: Vec<IssueItem> = self.persona_empty();

        let combined_vector: Vec<IssueItem> = routines
            .into_iter()
            .chain(superstates)
            .chain(states)
            .chain(intents)
            .chain(flow)
            .collect();

        combined_vector
    }

    fn btree_to_vec<V>(source: &'a BTreeMap<&'a str, V>) -> Vec<IssueItem<'a>>
    where
        V: Empty,
    {
        source.values().filter_map(|r| r.empty()).collect::<Vec<IssueItem>>()
    }

    fn persona_empty(&self) -> Vec<IssueItem<'_>> {
        if self.persona.is_empty() {
            vec![IssueItem::NoPersona]
        } else {
            vec![]
        }
    }
}

trait Empty {
    fn empty(&self) -> Option<IssueItem>;
}

impl<'a> Empty for Routine<'a> {
    fn empty(&self) -> Option<IssueItem<'a>> {
        if self.routine_name.is_empty()
            || self.max_says_at_once == 0
            || self.the_track.is_empty()
            || self.order_superstates.is_empty()
        {
            Some(IssueItem::EmptyField((
                self.routine_name,
                ConvItem::Routine,
            )))
        } else {
            None
        }
    }
}

impl<'a> Empty for Superstate<'a> {
    fn empty(&self) -> Option<IssueItem<'a>> {
        if self.superstate_name.is_empty() || self.states.is_empty() || self.description.is_empty()
        {
            Some(IssueItem::EmptyField((
                self.superstate_name,
                ConvItem::SuperState,
            )))
        } else {
            None
        }
    }
}

impl<'a> Empty for State<'a> {
    fn empty(&self) -> Option<IssueItem<'a>> {
        if self.state_name.is_empty()
            || (self.intents.is_empty() &&
                !matches!(self.state_type, ResponseType::Responsive) &&
                !matches!(self.state_type, ResponseType::Connective))
            // responsive and connective intents are allowed to have no intent activation
            || self.say_annotation.is_empty()
            || self.say.is_empty()
            || self.say.iter().any(|s| s.is_empty())
            || self.over_iterated_say.is_empty() && !are_same_variant(&self.state_type, &ResponseType::Connective)
            || self.over_iterated_say.iter().any(|os| os.is_empty())
        {
            Some(IssueItem::EmptyField((self.state_name, ConvItem::State)))
        } else {
            None
        }
    }
}

impl<'a> Empty for Intent<'a> {
    fn empty(&self) -> Option<IssueItem<'a>> {
        if self.intent_name.is_empty()
            || self.intent_annotation.is_empty()
            || self.keywords.is_empty()
            || self.adjacent.is_empty()
            || self.keywords.iter().any(|w| w.is_empty())
        {
            Some(IssueItem::EmptyField((self.intent_name, ConvItem::Intent)))
        } else {
            None
        }
    }
}
