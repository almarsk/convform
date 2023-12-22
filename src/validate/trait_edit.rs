use super::super::Flow;
use super::helper_structs_validate::{ConvItem, IssueItem, MissRef};
use crate::flow::{Intent, State};
use std::default::Default;

pub trait Edit<'a> {
    fn edit(&mut self, i: &IssueItem<'a>);
    fn add_item(&mut self, item: &MissRef<'a>);
    fn remove_item(&mut self, item: &(&'a str, ConvItem));
}

impl<'a> Edit<'a> for Flow<'a> {
    fn edit(&mut self, i: &IssueItem<'a>) {
        match i {
            IssueItem::MissingReference(m) => {
                println!("Adding {:?} called {}.", m.typ, m.name);
                self.add_item(m)
            }
            IssueItem::UnusedDeclared(m) => {
                println!("Removing {:?} called {}.", m.1, m.0);
                self.remove_item(m)
            }
            IssueItem::MissingReactionToSilence(i) => match *i {
                "state" => {
                    println!("Adding no input response state");
                    self.states
                        .insert("no input response", State::new("no input response"));
                }
                "intent" => {
                    println!("Adding no input intent");
                    self.intents.insert("no input", Intent::new("no input"));
                }
                _ => println!("nonexistent silence related issue: {}", i),
            },
            _ => println!("Something is being edited on the flow that shouldn't be."),
        }
    }

    fn add_item(&mut self, item: &MissRef<'a>) {
        match item.typ {
            ConvItem::State => {
                self.states.insert(item.name, State::new(item.name));
            }
            ConvItem::Intent => {
                self.intents.insert(item.name, Intent::new(item.name));
            }
            _ => {
                println!("something weird is going on")
            }
        };
    }

    fn remove_item(&mut self, item: &(&'a str, ConvItem)) {
        match item.1 {
            ConvItem::State => {
                self.states.remove(item.0);
            }
            ConvItem::Intent => {
                self.intents.remove(item.0);
            }
            _ => {
                println!("something weird is going on")
            }
        };
    }
}

impl<'a> State<'a> {
    fn new(state_name: &'a str) -> Self {
        State {
            state_name,
            iteration: 1,
            ..Default::default()
        }
    }
}
impl<'a> Intent<'a> {
    fn new(intent_name: &'a str) -> Self {
        Intent {
            intent_name,
            adjacent: vec!["$"],
            ..Default::default()
        }
    }
}
