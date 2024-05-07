import { useContext, useEffect, useState } from "react";
import myRequest from "../../myRequest";
import { Link, useParams } from "react-router-dom";
import { IssuesContext } from "../../IssuesContext";

const states = {
  0: "valid",
  1: "invalid",
  2: "unknown",
};

const ConversationContent = ({
  activeConversation,
  setActiveCStatusId,
  activeCStatusId,
}) => {
  const { flow } = useParams();
  const { setIssues, setTestCStatus } = useContext(IssuesContext);
  const [valid, setValid] = useState(0);

  useEffect(() => {
    myRequest("/proof", { flow: flow }).then((e) => {
      if (e.message === "invalid path") {
        setValid(2);
      } else if (!e.success) {
        setValid(1);
      }
    });
    localStorage.setItem("testCStatus", null);
  }, []);

  return (
    <>
      <ul className="conversation-content">
        {activeConversation.conversation.map((turn, i) =>
          turn.reply ? (
            <div
              key={i}
              className={`turn
                ${i === activeCStatusId ? "highlighted" : ""}
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
                      setIssues("inspect cstatus");
                    }}
                    onMouseLeave={() => setIssues("")}
                    onClick={() => {
                      setActiveCStatusId(i);
                    }}
                  >
                    🔬
                  </button>
                )}
                {states[valid] == "valid" && turn.who === "bot" && (
                  <Link to={`/admin/test/${flow}`}>
                    <button
                      className="submit"
                      onMouseOver={() => {
                        setIssues("");
                        setIssues("examine cstatus");
                      }}
                      onMouseLeave={() => setIssues("")}
                      onClick={() => {
                        const testCStatus = {
                          flow: flow,
                          cstatus: activeConversation.conversation[i].cstatus,
                          speech: nextSpeech(activeConversation, i),
                        };
                        const string_cstatus = JSON.stringify(testCStatus);
                        localStorage.setItem("testCStatus", string_cstatus);
                        setTestCStatus(testCStatus);
                      }}
                    >
                      🚀
                    </button>
                  </Link>
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

function nextSpeech(activeConversation, i) {
  const next = activeConversation.conversation[i + 1];
  return next ? next.reply : "";
}
