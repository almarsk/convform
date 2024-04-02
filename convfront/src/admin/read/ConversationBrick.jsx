const ConversationBrick = ({
  convo,
  convoId,
  setActiveConversationId,
  flow,
}) => {
  const date = (date) => {
    return `on ${date.getDate()}/${date.getMonth()}/${date.getFullYear().toString().slice(-2)}`;
  };

  return (
    <div
      className="bot-brick convo-brick"
      onClick={() => {
        setActiveConversationId(convoId);
      }}
    >
      <div>
        <div>{convo.nick}</div>
        <div>
          talked to {flow} {date(new Date(convo.start))}{" "}
          {convo.rating && "and rated " + convo.rating}
        </div>
      </div>
    </div>
  );
};

export default ConversationBrick;
