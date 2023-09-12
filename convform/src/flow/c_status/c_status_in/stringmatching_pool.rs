use super::get_stringmatching_pool::ToMatch;
use super::CStatusIn;

#[derive(Clone)]
pub struct StringMatchingPool<'a> {
    keywords_adjacent_pairs: Vec<ToMatch<'a>>,
    c_status_in: CStatusIn<'a>,
}

impl<'a> StringMatchingPool<'a> {
    pub fn new(csi: CStatusIn<'a>, kap: Vec<ToMatch<'a>>) -> StringMatchingPool<'a> {
        StringMatchingPool {
            keywords_adjacent_pairs: kap,
            c_status_in: csi,
        }
    }

    pub fn get_kaps(self) -> Vec<ToMatch<'a>> {
        self.keywords_adjacent_pairs
    }

    pub fn get_csi(&self) -> CStatusIn<'a> {
        self.c_status_in.clone()
    }
}
