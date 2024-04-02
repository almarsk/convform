import { useContext } from "react";
import MenuButton from "../MenuButton";
import { Link, useParams } from "react-router-dom";
import { IssuesContext } from "../../IssuesContext";

const ConversationContent = ({
  activeConversation,
  setActiveCStatusId,
  activeCStatusId,
}) => {
  const { flow } = useParams();
  const { setIssues, setTestCStatus } = useContext(IssuesContext);
  return (
    <>
      <ul className="conversation-content">
        {activeConversation.conversation.map((turn, i) =>
          turn.reply ? (
            <div
              key={i}
              className={`turn
                ${i === activeCStatusId ? (i == 1 ? "highlighted" : "highlighted-bot") : ""}
                ${i === activeCStatusId - 1 && typeof activeCStatusId == "number" ? "highlighted-human" : ""}

                `}
            >
              <div className="turn-element">
                {turn.who === "bot" ? "🤖: " : "🗣️: "}
              </div>
              <div className="turn-element">
                {turn.reply}
                <i>
                  {turn.who === "human" &&
                    " (after " + turn.reaction_ms + "ms)"}
                </i>
              </div>
              <div className="cstatus-menu">
                {turn.who === "bot" && (
                  <button
                    className="submit"
                    onMouseOver={() => {
                      setIssues("");
                      setIssues("read cstatus");
                    }}
                    onMouseLeave={() => setIssues("")}
                    onClick={() => {
                      setActiveCStatusId(i);
                    }}
                  >
                    🔬
                  </button>
                )}
                {true && turn.who === "bot" && (
                  <div
                    onClick={() =>
                      setTestCStatus({
                        flow: flow,
                        cstatus: activeConversation.conversation[i].cstatus,
                        lastSpeech:
                          activeConversation.conversation[i].reply || "",
                      })
                    }
                  >
                    <button
                      className="submit"
                      onMouseOver={() => {
                        setIssues("");
                        setIssues("read cstatus");
                      }}
                      onMouseLeave={() => setIssues("")}
                      onClick={() => {
                        setActiveCStatusId(i);
                      }}
                    >
                      <Link to={`/admin/test/${flow}`}>🚀</Link>
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            ""
          ),
        )}
      </ul>
      <hr className="end"></hr>
    </>
  );
};

export default ConversationContent;
