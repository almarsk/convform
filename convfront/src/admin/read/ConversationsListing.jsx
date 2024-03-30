import ConversationBrick from "./ConversationBrick";
import downloadConvos from "./downloadConvos";
import MenuButton from "../MenuButton";

const ConversationsListing = ({ setActiveConversationId, convos, flow }) => {
  return (
    <div className="read-container">
      <div className="read-item">
        <MenuButton
          hoverText={"export conversations with" + flow}
          click={() => downloadConvos(convos, flow)}
          icon={"📥"}
        ></MenuButton>
      </div>
      <div className="conversations-container">
        {convos &&
          convos.map((c, i) => (
            <ConversationBrick
              key={i}
              convo={c}
              convoId={i}
              setActiveConversationId={setActiveConversationId}
              flow={flow}
            />
          ))}
      </div>
    </div>
  );
};

export default ConversationsListing;
