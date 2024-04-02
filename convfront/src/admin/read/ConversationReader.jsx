import { useEffect } from "react";
import ConversationNavbar from "./ConversationNavbar";
import ConversationMetaInfo from "./ConversationMetaInfo";
import ConversationContent from "./ConversationContent";

const ConversationReader = ({
  activeConversation,
  setActiveConversationId,
  activeConversationId,
  setActiveCStatusId,
  activeCStatusId,
  nextConversation,
  prevConversation,
}) => {
  useEffect(() => {
    localStorage.setItem("activeConversationId", activeConversationId);
  });

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
              Object.entries(
                activeConversation.conversation[activeCStatusId].cstatus,
              ).map((item, index) => (
                <pre className="cstatus-item" key={index}>
                  {index !== 0 && <hr className="end" />}
                  {item[0] + ": "} {JSON.stringify(item[1], null, 2)}
                </pre>
              ))}
          </div>
        </div>
      </div>
    );
  }
};

export default ConversationReader;
