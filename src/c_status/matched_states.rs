use super::super::c_status::CStatusIn;
use super::stringmatching_pool::GroupingInfo;

#[derive(Debug)]
pub struct MatchedStates<'a> {
    pub matched_states: Vec<MatchItem<'a>>,
    pub c_status_in: CStatusIn,
}

#[derive(Clone, Debug)]
pub struct MatchItem<'a> {
    pub intent: &'a str,
    pub grouping: GroupingInfo<'a>,
    states: Vec<&'a str>,
    pub index_start: usize,
    pub answer_to: &'a [&'a str],
    // add context storage
}

impl<'a> MatchItem<'a> {
    pub fn new(
        _intent: &'a str,
        grouping: GroupingInfo<'a>,
        states: Vec<&'a str>,
        index_start: usize,
        answer_to: &'a [&str],
    ) -> Self {
        MatchItem {
            intent: _intent,
            grouping,
            states,
            index_start,
            answer_to,
        }
    }
    pub fn get_index(&self) -> usize {
        self.index_start
    }
    pub fn get_states(&self) -> Vec<&'a str> {
        self.states.clone()
    }
}

impl<'a> MatchedStates<'a> {
    pub fn get_states_and_csi(self) -> (Vec<MatchItem<'a>>, CStatusIn) {
        (self.matched_states, self.c_status_in)
    }

    pub fn get_usage(csi: &'a CStatusIn, state: &'a str) -> &'a usize {
        if let Some(usage) = csi.states_usage.get(state) {
            usage
        } else {
            &0
        }
    }
}
