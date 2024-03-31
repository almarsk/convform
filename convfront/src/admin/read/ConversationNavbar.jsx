const ConversationNavbar = ({
  prevConversation,
  setActiveConversationId,
  nextConversation,
}) => {
  return (
    <div className="navbar">
      {prevConversation ? (
        <button className="submit" onClick={prevConversation}>
          ◀
        </button>
      ) : (
        <div className="spacer" />
      )}
      <button
        className="submit"
        onClick={() => {
          localStorage.setItem("activeConversationId", null);
          setActiveConversationId(null);
        }}
      >
        ↖︎
      </button>
      {nextConversation ? (
        <button className="submit" onClick={nextConversation}>
          ▶
        </button>
      ) : (
        <div className="spacer" />
      )}
    </div>
  );
};

export default ConversationNavbar;
