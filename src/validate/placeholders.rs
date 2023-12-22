use super::{
    super::Flow,
    helper_structs_validate::{ConvItem, IssueItem},
};

impl<'a> Flow<'a> {
    pub fn placeholder_in_state(&self) -> Vec<IssueItem> {
        self.states
            .iter()
            .flat_map(|(state_name, state)| {
                state.intents.iter().filter_map(|(intent_id, s_adjacents)| {
                    self.intents.get(intent_id).and_then(|intent_info| {
                        if s_adjacents.contains(&"$")
                            && (intent_info.adjacent.is_empty()
                                || intent_info.adjacent.iter().all(|intent| *intent == "$"))
                        {
                            Some(IssueItem::DoublePlaceholder(
                                ConvItem::State,
                                state_name,
                                intent_id,
                            ))
                        } else {
                            None
                        }
                    })
                })
            })
            .collect()
    }

    pub fn placeholder_in_intent(&self) -> Vec<IssueItem> {
        self.intents
            .iter()
            .flat_map(|(state_name, state)| {
                state
                    .context_intents
                    .iter()
                    .filter_map(|(intent_id, s_adjacents)| {
                        self.intents.get(intent_id).and_then(|intent_info| {
                            if s_adjacents.contains(&"$")
                                && (intent_info.adjacent.is_empty()
                                    || intent_info.adjacent.iter().all(|intent| *intent == "$"))
                            {
                                Some(IssueItem::DoublePlaceholder(
                                    ConvItem::Intent,
                                    state_name,
                                    intent_id,
                                ))
                            } else {
                                None
                            }
                        })
                    })
            })
            .collect()
    }
}
