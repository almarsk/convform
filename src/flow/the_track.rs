use super::super::c_status::csi::CStatusIn;
use super::Flow;

pub fn next_from_the_track<'a>(flow: &'a Flow, csi: &mut CStatusIn) -> Option<&'a str> {
    crate::cnd_dbg!(&csi.states_usage);
    crate::cnd_dbg!(&csi.coda);

    if csi.coda {
        return None;
    }

    let usize_zero: usize = 0;
    let track_usage: Vec<(&'a str, usize)> = flow
        .the_track
        .iter()
        .rev()
        .fold(TrackUsage::new(), |mut acc, s| {
            acc.insert(s, csi.states_usage.get(*s).unwrap_or(&usize_zero));
            acc
        })
        .collect();

    crate::cnd_dbg!(&track_usage);

    let nonoveriterated_track_states: Vec<(&'a str, usize)> = track_usage
        .clone()
        .into_iter()
        .filter(|(track_state, track_usage)| {
            flow.states
                .values()
                .find(|flow_state| flow_state.state_name == *track_state)
                .unwrap()
                .iteration
                > *track_usage
        })
        .collect();

    if nonoveriterated_track_states.is_empty() {
        csi.coda = true;
        return Some(flow.coda);
    };

    Some(
        nonoveriterated_track_states
            .into_iter()
            .min_by_key(|(_s, u)| *u)
            .unwrap()
            .0,
    )
}

#[derive(Debug)]
struct TrackUsage<'a>(Vec<(&'a str, usize)>);

impl<'a> TrackUsage<'a> {
    fn new() -> TrackUsage<'a> {
        TrackUsage(vec![])
    }

    fn insert(&mut self, state: &'a str, usage: &usize) {
        self.0.push((state, *usage))
    }
}

impl<'a> Iterator for TrackUsage<'a> {
    type Item = (&'a str, usize);

    fn next(&mut self) -> Option<Self::Item> {
        self.0.pop()
    }
}
