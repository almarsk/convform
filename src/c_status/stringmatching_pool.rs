use super::CStatusIn;

#[derive(Clone, Debug)]
pub struct StringMatchingPool<'a> {
    pub keywords_adjacent_pairs: Vec<ToMatch<'a>>,
    pub csi: CStatusIn,
}

#[derive(Debug, Clone)]
pub struct ToMatch<'a> {
    pub intent_name: &'a str,
    pub grouping: GroupingInfo<'a>,
    pub keywords: Vec<String>,
    pub adjacent: Vec<&'a str>,
    pub answer_to: &'a [&'a str],
    // add context storage
}

#[derive(Debug)]
pub struct DecomposedIntentGrouping<'a> {
    pub name: &'a str,
    pub adjacent: Vec<&'a str>,
    pub grouping: GroupingInfo<'a>,
}

#[derive(Debug, Clone, Default)]
pub struct GroupingInfo<'a> {
    pub id: usize,
    pub number: usize,
    pub origin: &'a str,
}
