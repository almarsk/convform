import ConversationsListing from "./ConversationsListing";
import ConversationReader from "./ConversationReader";

import { useState } from "react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import myRequest from "../../myRequest";

const getActiveId = () => {
  const lc = localStorage.getItem("activeConversationId");
  return lc === "null" ? null : lc;
};

const ReadPage = () => {
  const [activeConversationId, setActiveConversationId] = useState(null);
  const { flow } = useParams();
  const [convos, setConvos] = useState([]);

  useEffect(() => {
    const getConvos = async () =>
      await myRequest("/convos", { flow: flow }).then((response) => {
        setConvos(response.data);
      });
    getConvos();

    setActiveConversationId(getActiveId());
  }, []);

  return (
    <>
      <b>reading {flow}</b>
      {activeConversationId || activeConversationId == 0 ? (
        <ConversationReader
          activeConversation={convos[activeConversationId]}
          setActiveConversationId={setActiveConversationId}
          nextConversation={
            activeConversationId < convos.length - 1
              ? () => {
                  setActiveConversationId(activeConversationId + 1);
                }
              : null
          }
          prevConversation={
            activeConversationId > 0
              ? () => setActiveConversationId(activeConversationId - 1)
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
    </>
  );
};

export default ReadPage;
