import { useContext } from "react";
import { IssuesContext } from "../../IssuesContext";

const ConversationNavbar = ({
  prevConversation,
  setActiveConversationId,
  nextConversation,
}) => {
  const { setIssues } = useContext(IssuesContext);

  return (
    <div className="navbar">
      {prevConversation ? (
        <button
          className="submit"
          onClick={prevConversation}
          onMouseOver={() => {
            setIssues("");
            setIssues("previous conversation");
          }}
          onMouseLeave={() => setIssues("")}
        >
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
        onMouseOver={() => {
          setIssues("");
          setIssues("back to listing");
        }}
        onMouseLeave={() => setIssues("")}
      >
        ↖︎
      </button>
      {nextConversation ? (
        <button
          className="submit"
          onClick={nextConversation}
          onMouseOver={() => {
            setIssues("");
            setIssues("next conversation");
          }}
          onMouseLeave={() => setIssues("")}
        >
          ▶
        </button>
      ) : (
        <div className="spacer" />
      )}
    </div>
  );
};

export default ConversationNavbar;
