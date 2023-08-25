use super::matched_states::MatchItem;

pub fn rhematize(mut m: Vec<MatchItem>) -> Vec<&str> {
    let _ = &mut m.sort_by_key(|ms| ms.get_index());
    m.into_iter().flat_map(|m| m.get_states().to_vec()).collect()
}
