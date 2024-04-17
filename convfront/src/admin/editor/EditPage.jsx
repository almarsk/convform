import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import myRequest from "../../myRequest";
import EditorPanel from "./EditorPanel";
import MenuButton from "../MenuButton";
import basename from "../../basename";

const EditPage = () => {
  const { flow } = useParams();
  const [proof, setProof] = useState("");
  const [valid, setValid] = useState(false);
  const [lastEvent, setLastEvent] = useState(`opened ${flow} editor`);
  const [flowData, setFlowData] = useState({});

  useEffect(() => {
    document.title = flow;
    return () => {
      document.title = "convform";
    };
  }, []);

  const fetchProof = async () => {
    const currentProof = await myRequest("/proof", { flow: flow });
    setProof(currentProof.message);
    setValid(currentProof.success);
  };

  const fetchItems = async () => {
    const sending = {
      flow: flow,
      func: "list",
    };
    myRequest("/convform", sending).then((e) => {
      e.data && setFlowData(e.data);
    });
  };

  useEffect(() => {
    fetchProof();
    fetchItems();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="editor-container">
      <h3 className="subheader">Editing {flow}</h3>
      <div className="panel-container">
        <div className="side-panel">
          <div>
            <b>{lastEvent ? `last event: ${lastEvent}` : ""}</b>
          </div>
          <ul className="proof-list">
            {proof &&
              proof.split("\n").map((message, i) => (
                <div className="proof-item" key={i}>
                  {message}
                </div>
              ))}
            {valid && (
              <MenuButton
                icon={"🚀"}
                hoverText={`redirect to ${flow}`}
                click={() => window.open(`${basename}/?flow=${flow}`, "_blank")}
              />
            )}
          </ul>
        </div>
        <EditorPanel
          initial="list-states"
          flow={flow}
          setLastEvent={setLastEvent}
          fetchProof={fetchProof}
          flowData={flowData}
          fetchItems={fetchItems}
        />
        <EditorPanel
          initial="list-intents"
          flow={flow}
          setLastEvent={setLastEvent}
          fetchProof={fetchProof}
          flowData={flowData}
          fetchItems={fetchItems}
        />
      </div>
    </div>
  );
};

EditPage.propTypes = {};

export default EditPage;
