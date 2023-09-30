use super::CStatusIn;
use super::Flow;
use super::StringMatchingPool;

use crate::flow::State;
use std::collections::BTreeMap;

#[derive(Debug, Clone)]
pub struct ToMatch<'a> {
    pub intent_name: &'a str,
    keywords: &'a [&'a str],
    pub adjacent: Vec<&'a str>,
    pub answer_to: &'a [&'a str],
}

impl<'a> ToMatch<'a> {
    pub fn new(
        intent_name: &'a str,
        keywords: &'a [&'a str],
        adjacent: Vec<&'a str>,
        answer_to: &'a [&'a str],
    ) -> Self {
        ToMatch {
            intent_name,
            keywords,
            adjacent,
            answer_to,
        }
    }

    pub fn keywords(&self) -> &[&'a str] {
        self.keywords
    }

    pub fn answer_to(&self) -> &[&'a str] {
        self.answer_to
    }
}

impl<'a> CStatusIn<'a> {
    pub fn get_stringmatching_pool(self, flow: &'a Flow<'a>) -> StringMatchingPool<'a> {
        let states = self.last_states.clone();

        let full_last_states: Vec<&'a State> = states
            .iter()
            .map(|ls| flow.states.iter().find(|fs| fs.0 == ls).unwrap())
            .map(|s| s.1)
            .collect();

        let last_states_intents: Vec<&'a BTreeMap<&str, Vec<&str>>> =
            full_last_states.iter().map(|fs| &fs.intents).collect();

        let mut unique_last_states_intents = BTreeMap::<&str, Vec<&str>>::new();

        last_states_intents.iter().for_each(|b| {
            b.iter().for_each(|i| {
                let entry = unique_last_states_intents.entry(i.0).or_insert(vec![]);
                i.1.iter().for_each(|adjacent| {
                    if !entry.contains(adjacent) {
                        entry.push(adjacent)
                    }
                })
            });
        });

        println!("{:#?}", unique_last_states_intents);

        // decompose combined intents here and keep the info about the pairs
        // only one of the combined intents will get the adjacent states
        // the list of grouping will be added in Stringmatchingpool (new arm)
        // the groupings list will be structured like - main; empty, so the pairing is easy
        // add answer to only if the intent isnt duplicate
        //
        // add annotation to ToMatch so gpt can be prompted easily

        let to_match_sequence: Vec<ToMatch> = unique_last_states_intents
            .into_iter()
            .map(|i| {
                ToMatch::new(
                    i.0,
                    get_keywords(flow, i.0),
                    get_adjacent((i.0, i.1), flow),
                    get_answer_to(flow, i.0),
                )
            })
            .collect();

        let smp = StringMatchingPool::new(self, to_match_sequence);
        smp
    }
}

fn get_keywords<'a>(flow: &'a Flow, intent: &str) -> &'a [&'a str] {
    if let Some(i) = flow
        .intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| &f_intent.1.keywords)
    {
        i
    } else {
        println!("{intent}");
        &[]
    }
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
    //
    // the function gets the state defined adjacent states in intent.1
    // if there is "$" in the states intents, it finds the default adjacent (intent defined) states
    // and puts those together
    if intent.1.contains(&"$") {
        let current_intent = flow.intents.iter().find(|i| i.0 == &intent.0).unwrap();
        let mut aditional_adjacent_states = current_intent.1.adjacent.clone();
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
