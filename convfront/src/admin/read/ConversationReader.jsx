import { useEffect } from "react";
import ConversationNavbar from "./ConversationNavbar";
import ConversationMetaInfo from "./ConversationMetaInfo";
import ConversationContent from "./ConversationContent";
import { useContext } from "react";
import { IssuesContext } from "../../IssuesContext";
import CStatusReader from "./CStatusReader";

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
          <CStatusReader
            cStatusStructure={cStatusStructure}
            conversation={
              activeCStatusId &&
              activeConversation.conversation[activeCStatusId]
            }
          />
        </div>
      </div>
    );
  }
};

export default ConversationReader;
