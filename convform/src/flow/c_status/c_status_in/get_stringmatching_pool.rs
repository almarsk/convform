use super::CStatusIn;
use super::Flow;
use super::StringMatchingPool;

use crate::flow::State;
use std::collections::BTreeMap;

#[derive(Debug, Clone)]
pub struct ToMatch<'a> {
    pub intent_name: &'a str,
    pub grouping: GroupingInfo<'a>,
    keywords: &'a [&'a str],
    pub adjacent: Vec<&'a str>,
    pub answer_to: &'a [&'a str],
}

impl<'a> ToMatch<'a> {
    pub fn new(
        intent_name: &'a str,
        grouping: GroupingInfo<'a>,
        keywords: &'a [&'a str],
        adjacent: Vec<&'a str>,
        answer_to: &'a [&'a str],
    ) -> Self {
        ToMatch {
            intent_name,
            grouping,
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
        let mut states = self.last_states.clone();
        states.extend(get_global_states(&self, flow));

        let full_last_states: Vec<&'a State> = states
            .iter()
            .map(|ls| flow.states.iter().find(|fs| fs.0 == ls).unwrap())
            .map(|s| s.1)
            .collect();

        let last_states_intents: Vec<(&'a BTreeMap<&str, Vec<&str>>, &'a str)> = full_last_states
            .iter()
            .map(|fs| (&fs.intents, fs.state_name))
            .collect();

        let mut unique_last_states_intents = BTreeMap::<&str, (Vec<&str>, &'a str)>::new();

        last_states_intents.iter().for_each(|b| {
            b.0.iter().for_each(|i| {
                let entry = unique_last_states_intents.entry(i.0).or_insert((vec![], b.1));
                i.1.iter().for_each(|adjacent| {
                    if !entry.0.contains(adjacent) {
                        entry.0.push(adjacent)
                    }
                })
            });
        });

        // println!("{:#?}", unique_last_states_intents);

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
                            origin: i.1 .1, // !!! fix
                        },
                    });
                });
            });

        //println!("{:#?}", unique_last_decomposed_intents);

        // decompose combined intents here and keep the info about the pairs
        // only one of the combined intents will get the adjacent states
        // the list of grouping will be added in Stringmatchingpool (new arm)
        // the groupings list will be structured like - main; empty, so the pairing is easy
        // add answer to only if the intent isnt duplicate
        //
        // add annotation to ToMatch so gpt can be prompted easily

        let to_match_sequence: Vec<ToMatch> = unique_last_decomposed_intents
            .into_iter()
            .map(|i| {
                ToMatch::new(
                    i.name,
                    i.grouping,
                    get_keywords(flow, i.name),
                    get_adjacent((i.name, i.adjacent), flow),
                    get_answer_to(flow, i.name),
                )
            })
            .collect();

        let smp = StringMatchingPool::new(self, to_match_sequence);
        //println!("{:#?}", smp);
        smp
    }
}

fn get_keywords<'a>(flow: &'a Flow, intent: &str) -> &'a [&'a str] {
    flow.intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| &f_intent.1.keywords)
        .unwrap()
}

fn get_answer_to<'a>(flow: &'a Flow, intent: &str) -> &'a [&'a str] {
    flow.intents
        .iter()
        .find(|(_, i)| intent == i.intent_name)
        .map(|f_intent| &f_intent.1.answer_to)
        .unwrap()
}

fn get_global_states<'a>(csi: &CStatusIn, flow: &'a Flow) -> Vec<&'a str> {
    let superstate_name = csi.superstate;
    let last_states = &csi.last_states;
    let full_superstate = flow
        .superstates
        .iter()
        .find(|superstate| superstate.0 == &superstate_name)
        .unwrap();
    let relevant_states = &full_superstate.1.states;
    let absent_states: Vec<_> =
        relevant_states.iter().filter(|s| !last_states.contains(s)).collect();
    absent_states
        .iter()
        .filter(|s| flow.states.iter().find(|fs| &fs.0 == *s).unwrap().1.superstate_global)
        .copied()
        .copied()
        .collect()
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

#[derive(Debug)]
struct DecomposedIntentGrouping<'a> {
    name: &'a str,
    adjacent: Vec<&'a str>,
    grouping: GroupingInfo<'a>,
}

#[derive(Debug, Clone, Default)]
pub struct GroupingInfo<'a> {
    pub id: usize,
    pub number: usize,
    pub origin: &'a str,
}
