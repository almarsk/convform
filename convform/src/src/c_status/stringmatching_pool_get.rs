use super::super::flow::State;
use super::stringmatching_pool::{
    DecomposedIntentGrouping, GroupingInfo, StringMatchingPool, ToMatch,
};
use super::CStatusIn;
use super::Flow;
use std::collections::BTreeMap;

impl<'a> CStatusIn {
    pub fn get_stringmatching_pool(self, flow: &'a Flow<'a>) -> StringMatchingPool<'a> {
        let states = self.last_states.clone();

        let full_last_states: Vec<&'a State> = states
            .iter()
            .map(|ls| flow.states.iter().find(|fs| fs.0 == ls).unwrap())
            .map(|s| s.1)
            .collect();

        let last_states_intents: Vec<(&'a BTreeMap<&str, Vec<&str>>, &'a str)> = full_last_states
            .iter()
            .map(|fs| (&fs.intents, fs.state_name))
            .collect();

        // last_states_intents be mut
        // get context_intents and it has to contain the origin state + remark its context
        // BTreeMap of intent

        let mut unique_last_states_intents = BTreeMap::<&str, (Vec<&str>, &'a str)>::new();

        last_states_intents.iter().for_each(|b| {
            b.0.iter().for_each(|i| {
                let entry = unique_last_states_intents
                    .entry(i.0)
                    .or_insert((vec![], b.1));
                i.1.iter().for_each(|adjacent| {
                    if !entry.0.contains(adjacent) {
                        entry.0.push(adjacent)
                    }
                })
            });
        });

        crate::cnd_dbg!(&unique_last_states_intents);

        let mut unique_last_decomposed_intents: Vec<DecomposedIntentGrouping> = vec![];
        unique_last_states_intents
            .into_iter()
            .enumerate()
            .for_each(|(index, i)| {
                let grouping = i.0.split('+').collect::<Vec<&'a str>>();
                grouping.clone().into_iter().for_each(|di| {
                    unique_last_decomposed_intents.push(DecomposedIntentGrouping {
                        name: di.trim(),
                        adjacent: i.1 .0.clone(),
                        grouping: GroupingInfo {
                            id: index,
                            number: grouping.len(),
                            origin: i.1 .1,
                        },
                    });
                });
            });

        crate::cnd_dbg!(&unique_last_decomposed_intents);

        // add annotation to ToMatch so gpt can be prompted easily

        dbg!("add context storage");
        let mut to_match_sequence: Vec<ToMatch> = unique_last_decomposed_intents
            .into_iter()
            .map(|i| ToMatch {
                intent_name: i.name,
                grouping: i.grouping,
                keywords: get_keywords(flow, i.name),
                adjacent: get_adjacent((i.name, i.adjacent), flow),
                answer_to: get_answer_to(flow, i.name),
                // add context storage + get_context func (will return name, vec or adjacent and origin)
            })
            .collect();

        // check for empty user reply
        if self.user_reply.is_empty()
            && self.bot_turns > 0
            && !to_match_sequence
                .iter()
                .any(|kap| kap.intent_name == "no input")
        {
            to_match_sequence.push(ToMatch {
                intent_name: "no input",
                keywords: vec![String::from("")],
                adjacent: vec!["$"],
                answer_to: &[],
                grouping: GroupingInfo {
                    id: 0,
                    number: 0,
                    origin: "no input response",
                },
            })
        }

        StringMatchingPool {
            keywords_adjacent_pairs: to_match_sequence,
            csi: self,
        }
    }
}

fn get_keywords(flow: &Flow, intent: &str) -> Vec<String> {
    flow.intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| f_intent.1.keywords.clone())
        .unwrap()
}

fn get_answer_to<'a>(flow: &'a Flow, intent: &str) -> &'a [&'a str] {
    flow.intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| &f_intent.1.answer_to)
        .unwrap()
}

fn get_adjacent<'a>(intent: (&str, Vec<&'a str>), flow: &'a Flow<'a>) -> Vec<&'a str> {
    // dollar sign signifies default adjacent state which is present in flow definition

    // the function gets the state defined adjacent states in intent.1
    // if there is "$" in the states intents, it finds the default adjacent (intent defined) states
    // and puts those together
    if intent.1.contains(&"$") {
        let current_intent = flow.intents.iter().find(|i| i.0 == &intent.0).unwrap();
        let mut aditional_adjacent_states = current_intent.1.adjacent.clone();
        // the order here doesn't matter, depends on index of matching sector
        aditional_adjacent_states.extend(intent.1);
        aditional_adjacent_states
            .iter()
            .filter(|s| s != &&"$")
            .copied()
            .collect()
    } else {
        intent.1.to_vec()
    }
}
