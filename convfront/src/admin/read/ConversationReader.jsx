import { useEffect } from "react";
import ConversationNavbar from "./ConversationNavbar";
import ConversationMetaInfo from "./ConversationMetaInfo";
import ConversationContent from "./ConversationContent";
import { useContext } from "react";
import { IssuesContext } from "../../IssuesContext";

const ConversationReader = ({
  activeConversation,
  setActiveConversationId,
  activeConversationId,
  setActiveCStatusId,
  activeCStatusId,
  nextConversation,
  prevConversation,
}) => {
  const { cStatusStructure } = useContext(IssuesContext);

  useEffect(() => {
    localStorage.setItem("activeConversationId", activeConversationId);
  }, []);

  //!!activeConversation && console.log(activeConversation);

  if (!activeConversation) {
    setActiveConversationId(null);
  } else {
    return (
      <div className="reader-container">
        <ConversationNavbar
          setActiveConversationId={setActiveConversationId}
          nextConversation={nextConversation}
          prevConversation={prevConversation}
        />
        <div className="conversation-reader">
          <div className="turns-reader">
            <ConversationMetaInfo activeConversation={activeConversation} />
            <ConversationContent
              activeConversation={activeConversation}
              setActiveCStatusId={setActiveCStatusId}
              activeCStatusId={activeCStatusId}
            />
          </div>
          <div className="turns-reader">
            {activeCStatusId &&
              activeConversation.conversation[activeCStatusId] &&
              cStatusStructure.map(([key], index) => {
                const value =
                  activeConversation.conversation[activeCStatusId].cstatus[key];
                return (
                  <pre className="cstatus-item" key={index}>
                    {index !== 0 && <hr className="end" />}
                    {key + ": "} {JSON.stringify(value, null, 2)}
                  </pre>
                );
              })}
          </div>
        </div>
      </div>
    );
  }
};

export default ConversationReader;
