import ConversationsListing from "./ConversationsListing";
import ConversationReader from "./ConversationReader";

import { useState } from "react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import myRequest from "../../myRequest";

const getActiveId = () => {
  const lc = localStorage.getItem("activeConversationId");
  return parseInt(lc);
};

const ReadPage = () => {
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [activeCStatusId, setActiveCStatusId] = useState(null);
  const [convos, setConvos] = useState(null);
  const { flow } = useParams();

  useEffect(() => {
    const getConvos = async () =>
      await myRequest("/convos", { flow: flow }).then((response) => {
        setConvos(response.data);
        setActiveConversationId(getActiveId());
      });
    getConvos();
  }, []);

  useEffect(() => {
    setActiveCStatusId(null);
  }, [activeConversationId]);

  return (
    <div>
      <b>reading {flow}</b>
      {activeConversationId || activeConversationId == 0 ? (
        <ConversationReader
          setActiveCStatusId={setActiveCStatusId}
          activeCStatusId={activeCStatusId}
          activeConversation={!!convos && convos[activeConversationId]}
          setActiveConversationId={setActiveConversationId}
          activeConversationId={activeConversationId}
          nextConversation={
            activeConversationId < convos.length - 1
              ? () => {
                  localStorage.setItem(
                    "activeConversationId",
                    activeConversationId + 1,
                  );
                  setActiveConversationId(activeConversationId + 1);
                }
              : null
          }
          prevConversation={
            activeConversationId > 0
              ? () => {
                  localStorage.setItem(
                    "activeConversationId",
                    activeConversationId - 1,
                  );
                  setActiveConversationId(activeConversationId - 1);
                }
              : null
          }
        />
      ) : (
        <ConversationsListing
          setActiveConversationId={setActiveConversationId}
          flow={flow}
          convos={convos}
        />
      )}
    </div>
  );
};

export default ReadPage;
