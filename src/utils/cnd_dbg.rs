#[macro_export]
macro_rules! cnd_dbg {
    ($value:expr) => {
        #[cfg(feature = "debug")]
        {
            dbg!($value);
        }
    };
}
