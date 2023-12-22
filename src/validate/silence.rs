use super::Flow;
use super::IssueItem;

impl<'a> Flow<'a> {
    pub fn silence(&self) -> Vec<IssueItem<'a>> {
        let missing_silence_response = self.states.iter().all(|(s, _)| *s != "no input response");
        let missing_silence_intent = self.intents.iter().all(|(s, _)| *s != "no input");
        let mut issues: Vec<IssueItem<'a>> = vec![];
        if missing_silence_response {
            issues.push(IssueItem::MissingReactionToSilence("state"))
        };
        if missing_silence_intent {
            issues.push(IssueItem::MissingReactionToSilence("intent"))
        };
        issues
    }
}
