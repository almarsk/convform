import ConversationNavbar from "./ConversationNavbar";

const ConversationReader = ({
  activeConversation,
  setActiveConversationId,
  nextConversation,
  prevConversation,
}) => {
  console.log(activeConversation);
  if (!activeConversation) {
    setActiveConversationId(null);
  } else {
    return (
      <>
        <ConversationNavbar
          setActiveConversationId={setActiveConversationId}
          nextConversation={nextConversation}
          prevConversation={prevConversation}
        />
        <div className="conversation-reader">
          <div className="turns-reader">
            <ul class="conversation-meta">
              <li>{activeConversation.nick}</li>
              <li>{activeConversation.start}</li>
              <li>{activeConversation.end}</li>
              <li>{activeConversation.aborted}</li>
              <li>{activeConversation.rating}</li>
              <li>{activeConversation.comment}</li>
            </ul>
            <ul class="conversation-content">
              {activeConversation.conversation.map((turn) =>
                turn.reply ? (
                  <p className="turn">
                    <p>{turn.who === "bot" ? "🤖: " : "🗣️: "}</p>
                    <p>{turn.reply}</p>
                  </p>
                ) : (
                  ""
                ),
              )}
            </ul>
            {/*JSON.stringify(activeConversation)*/} <br /> todo:
            <br /> click convos - info, repliky,
            <br /> bot turns have view cstate button,
          </div>
          <div className="turns-reader">
            <br /> cstate panel (active cstate state)
            <br /> link to testing in cstate panel if !! active cstate and if
            flow is valid
          </div>
        </div>
      </>
    );
  }
};

export default ConversationReader;
