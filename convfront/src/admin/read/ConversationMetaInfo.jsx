function processMetaInfo(acid, item) {
  if (item == "start" || item == "end") return acid[item].split(".")[0];
  if (item == "aborted") return acid[item] ? "aborted" : "not aborted";
  return acid[item];
}

const ConversationMetaInfo = ({ activeConversation }) => {
  return (
    <ul className="conversation-meta">
      {["nick", "start", "end", "aborted", "rating", "comment"].map(
        (item, i) => {
          return (
            <li key={i} className="meta-turn">
              <div>
                <b>{item}: </b>
              </div>
              <div>
                {processMetaInfo(activeConversation, item) || `no ${item}`}
              </div>
            </li>
          );
        },
      )}
    </ul>
  );
};

export default ConversationMetaInfo;
