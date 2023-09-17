use super::super::{Intent, Routine, State, Superstate};
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
}

#[derive(Debug)]
pub enum IssueItem<'a> {
    NoPersona,
    MissingStateIntro((&'a str, &'a str)),
    MissingReference(MissRef<'a>),
    UnusedDeclared((&'a str, ConvItem)),
    EmptyField((&'a str, ConvItem)),
    DifferentKeyName((&'a str, &'a str, ConvItem)),
    DoublePlaceholder(&'a str, &'a str),
    FaultyRegex(FRgx<'a>),
    InvalidPrompt((&'a str, &'a str)),
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
    Routine,
    SuperState,
    State,
    Intent,
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

impl<'a> ValidateReferences<'a> for Routine<'a> {
    fn get_refs(&self) -> Vec<ValidationReference<'a>> {
        self.order_superstates
            .iter()
            .map(|superstate| ValidationReference {
                origin_name: vec![self.routine_name],
                origin_type: ConvItem::Routine,
                item_name: superstate,
                item_type: ConvItem::SuperState,
            })
            .collect()
    }

    fn get_name(&self) -> (&'a str, &'a str) {
        (self.routine_name, "routine")
    }
}

impl<'a> ValidateReferences<'a> for Superstate<'a> {
    fn get_refs(&self) -> Vec<ValidationReference<'a>> {
        self.states
            .iter()
            .map(|state| ValidationReference {
                origin_name: vec![self.superstate_name],
                origin_type: ConvItem::SuperState,
                item_name: state,
                item_type: ConvItem::State,
            })
            .collect()
    }

    fn get_name(&self) -> (&'a str, &'a str) {
        (self.superstate_name, "superstate")
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
        let mut intent_refs = adjacent.clone();
        intent_refs.extend(answer_to);
        intent_refs
    }

    fn get_name(&self) -> (&'a str, &'a str) {
        (self.intent_name, "intent")
    }
}

pub fn are_same_variant<T>(a: &T, b: &T) -> bool {
    std::mem::discriminant(a) == std::mem::discriminant(b)
}
