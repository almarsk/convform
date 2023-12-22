use super::super::flow::{the_track::next_from_the_track, Flow};
use super::CStatusIn;

pub fn handle_noninitiative<'a>(
    ordered: &mut Vec<&'a str>,
    flow: &'a Flow<'a>,
    csi: &mut CStatusIn,
) {
    if csi.turns_since_initiative < csi.initiativity {
        crate::cnd_dbg!("not yet time to add initiativity");
        return;
    }
    if csi.bot_turns > 0 {
        // look at each state from the track
        // find the next one
        // flow.the_track.iter().fold(); ....
        if let Some(next_state) = next_from_the_track(flow, csi) {
            ordered.push(next_state);
        }
    } else {
        ordered.push("state_intro")
    }

    // check if it has been long enough since initiativeness
    // add next from key states
}
