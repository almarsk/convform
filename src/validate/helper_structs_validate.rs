use super::super::flow::{Flow, Intent, ResponseType, State};
use regex::Error;

#[derive(Clone, Debug)]
pub struct ValidationReference<'a> {
    pub origin_name: Vec<&'a str>,
    pub origin_type: ConvItem,
    pub item_name: &'a str,
    pub item_type: ConvItem,
}

#[derive(Clone, Debug)]
pub struct ValidationDeclaration<'a> {
    pub item_name: &'a str,
    pub item_type: ConvItem,
    pub allow_unit: bool,
}

#[derive(Debug)]
pub enum IssueItem<'a> {
    NoPersona,
    MissingStateIntro,
    MissingReference(MissRef<'a>),
    UnusedDeclared((&'a str, ConvItem)),
    EmptyField((&'a str, ConvItem)),
    DifferentKeyName((&'a str, &'a str, ConvItem)),
    DoublePlaceholder(ConvItem, &'a str, &'a str),
    FaultyRegex(FRgx<'a>),
    InvalidPrompt((&'a str, &'a str)),
    ExtraSpace((&'a str, &'a str)),
    MissingReactionToSilence(&'a str),
}

#[derive(Debug)]
pub struct FRgx<'a> {
    pub kw: &'a str,
    pub wher: &'a str,
    pub err: Error,
}

#[derive(Debug)]
pub struct MissRef<'a> {
    pub typ: ConvItem,
    pub name: &'a str,
    pub wher: &'a Vec<&'a str>,
    pub otyp: ConvItem,
}

#[derive(Clone, Debug, Copy)]
pub enum ConvItem {
    State,
    Intent,
    Flow,
}

impl<'a> IssueItem<'a> {
    pub fn format_issues(&self) -> String {
        format!("{:?}\n", self)
    }
}

pub trait ValidateReferences<'a> {
    fn get_refs(&self) -> Vec<ValidationReference<'a>>;
    fn get_name(&self) -> (&'a str, &'a str);
}

impl<'a> ValidateReferences<'a> for Flow<'a> {
    fn get_refs(&self) -> Vec<ValidationReference<'a>> {
        self.the_track
            .iter()
            .map(|s| ValidationReference {
                origin_name: vec!["the track"],
                origin_type: ConvItem::Flow,
                item_name: s,
                item_type: ConvItem::State,
            })
            .chain(
                vec![ValidationReference {
                    origin_name: vec!["coda"],
                    origin_type: ConvItem::Flow,
                    item_name: self.coda,
                    item_type: ConvItem::State,
                }]
                .into_iter(),
            )
            .collect()
    }
    fn get_name(&self) -> (&'a str, &'a str) {
        (self.persona, "persona")
    }
}

impl<'a> ValidateReferences<'a> for State<'a> {
    fn get_refs(&self) -> Vec<ValidationReference<'a>> {
        let intent_refs: Vec<ValidationReference<'a>> = self
            .intents
            .iter()
            .flat_map(|i| {
                i.0.split('+')
                    .map(|i| i.trim())
                    .map(|intent_pair| ValidationReference {
                        origin_name: vec![self.state_name],
                        origin_type: ConvItem::State,
                        item_name: intent_pair,
                        item_type: ConvItem::Intent,
                    })
            })
            .collect();

        let state_refs: Vec<ValidationReference<'a>> = self
            .intents
            .iter()
            .flat_map(|intent_pair| {
                intent_pair
                    .1
                    .iter()
                    .filter(|state| **state != "$")
                    .map(|state| ValidationReference {
                        origin_name: vec![
                            "adjacent state in used intent",
                            self.state_name,
                            intent_pair.0,
                        ],
                        origin_type: ConvItem::Intent,
                        item_name: state,
                        item_type: ConvItem::State,
                    })
                    .collect::<Vec<ValidationReference<'a>>>()
            })
            .collect();
        let mut refs_to_validate = vec![];
        refs_to_validate.extend(intent_refs);
        refs_to_validate.extend(state_refs);
        refs_to_validate
    }

    fn get_name(&self) -> (&'a str, &'a str) {
        (self.state_name, "state")
    }
}

impl<'a> ValidateReferences<'a> for Intent<'a> {
    fn get_refs(&self) -> Vec<ValidationReference<'a>> {
        let adjacent: Vec<ValidationReference<'_>> = self
            .adjacent
            .iter()
            .filter(|state| **state != "$")
            .map(|state| ValidationReference {
                origin_name: vec!["adjacent", self.intent_name],
                origin_type: ConvItem::Intent,
                item_name: state,
                item_type: ConvItem::State,
            })
            .collect();
        let answer_to = self.answer_to.iter().map(|state| ValidationReference {
            origin_name: vec!["answer to state", self.intent_name],
            origin_type: ConvItem::Intent,
            item_name: state,
            item_type: ConvItem::State,
        });
        let context_intent_refs: Vec<ValidationReference<'a>> = self
            .context_intents
            .iter()
            .flat_map(|i| {
                i.0.split('+')
                    .map(|i| i.trim())
                    .map(|intent| ValidationReference {
                        origin_name: vec![self.intent_name],
                        origin_type: ConvItem::Intent,
                        item_name: intent,
                        item_type: ConvItem::Intent,
                    })
            })
            .collect();

        let context_adjacent: Vec<ValidationReference<'_>> = self
            .context_intents
            .iter()
            .flat_map(|(_, states)| states.iter().filter(|s| s != &&"$"))
            .map(|state| ValidationReference {
                origin_name: vec!["adjacent", self.intent_name],
                origin_type: ConvItem::Intent,
                item_name: state,
                item_type: ConvItem::State,
            })
            .collect();

        let mut intent_refs = adjacent.clone();
        intent_refs.extend(answer_to);
        intent_refs.extend(context_intent_refs);
        intent_refs.extend(context_adjacent);
        intent_refs
    }

    fn get_name(&self) -> (&'a str, &'a str) {
        (self.intent_name, "intent")
    }
}

pub fn are_same_variant<T>(a: &T, b: &T) -> bool {
    std::mem::discriminant(a) == std::mem::discriminant(b)
}

pub fn get_response_type<'a>(state: &str, flow: &'a Flow) -> &'a ResponseType {
    &flow
        .states
        .iter()
        .find(|s| s.0 == &state)
        .unwrap()
        .1
        .state_type
}
