use std::collections::BTreeMap;

pub fn default_vec<'a>() -> Vec<&'a str> {
    vec![]
}
pub fn default_btree<K, V>() -> BTreeMap<K, V> {
    BTreeMap::new()
}
pub fn default_iteration() -> usize {
    1
}
pub fn default_bool() -> bool {
    false
}
pub fn default_option_usize() -> Option<usize> {
    None
}
