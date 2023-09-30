use super::super::Flow;
use super::helper_structs_validate::{ConvItem, IssueItem, MissRef};
use crate::flow::{Intent, Routine, State, Superstate};
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
                println!("Need to add {:?} called {}.", m.typ, m.name);
                self.add_item(m)
            }
            IssueItem::UnusedDeclared(m) => {
                println!("Need to remove {:?} called {}.", m.1, m.0);
                self.remove_item(m)
            }
            _ => println!("Something is being edited on the flow that shouldn't be."),
        }
    }

    fn add_item(&mut self, item: &MissRef<'a>) {
        match item.typ {
            ConvItem::Routine => {
                self.routines.insert(item.name, Routine::new(item.name));
            }
            ConvItem::SuperState => {
                self.superstates.insert(item.name, Superstate::new(item.name));
            }
            ConvItem::State => {
                self.states.insert(item.name, State::new(item.name));
            }
            ConvItem::Intent => {
                self.intents.insert(item.name, Intent::new(item.name));
            }
        };
    }

    fn remove_item(&mut self, item: &(&'a str, ConvItem)) {
        match item.1 {
            ConvItem::Routine => {
                self.routines.remove(item.0);
            }
            ConvItem::SuperState => {
                self.superstates.remove(item.0);
            }
            ConvItem::State => {
                self.states.remove(item.0);
            }
            ConvItem::Intent => {
                self.intents.remove(item.0);
            }
        };
    }
}

impl<'a> Routine<'a> {
    fn new(routine_name: &'a str) -> Self {
        Routine {
            routine_name,
            ..Default::default()
        }
    }
}
impl<'a> Superstate<'a> {
    fn new(superstate_name: &'a str) -> Self {
        Superstate {
            superstate_name,
            ..Default::default()
        }
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
