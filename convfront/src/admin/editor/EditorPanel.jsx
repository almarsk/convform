import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import myRequest from "../../myRequest";
import "./editor.scss";

import AbstractForm from "./AbstractForm";
import Listing from "./Listing";
import EditorButtons from "./EditorButtons";
import { InputContextProvider } from "./InputContext";

const EditorPanel = ({
  initial,
  flow,
  setLastEvent,
  fetchProof,
  flowData,
  fetchItems,
}) => {
  const [activePanel, setActivePanel] = useState(initial);
  const [structure, setStructure] = useState({});
  const [activeElement, setActiveElement] = useState({});

  useEffect(() => {
    const fetchStructure = async () => {
      const structure_all = await myRequest("/structure", {}).then((e) => {
        return e;
      });
      setStructure(structure_all);
    };
    fetchStructure();
  }, [flowData]);

  const convform = ({ e, element, activeItem, setChanges }) => {
    e.preventDefault();

    const edit = async () => {
      await myRequest("/convform", {
        flow: flow,
        func: "edit",
        item_type: element,
        name: activeItem.name,
        data: activeItem,
      }).then((e) => {
        fetchProof();
        fetchItems();
        e.success
          ? setLastEvent(`edited ${element} ${activeItem.name || ""}`)
          : setLastEvent(`couldn't edit ${element} ${activeItem.name || ""}`);
      });
    };
    edit();
    setChanges(false);
  };

  return (
    <div className="panel">
      <EditorButtons setActivePanel={setActivePanel} />
      {activePanel === "state" ? (
        <InputContextProvider>
          <AbstractForm
            element={"state"}
            fields={structure.states || {}}
            flow={flow}
            elementData={
              flowData &&
              flowData.states.filter((f) => f.name === activeElement)[0]
            }
            setActivePanel={setActivePanel}
            handleSubmit={convform}
          />
        </InputContextProvider>
      ) : activePanel === "list-states" ? (
        <Listing
          elementType={"state"}
          fields={structure.states || {}}
          flow={flow}
          setActivePanel={setActivePanel}
          setActiveElement={setActiveElement}
          fetchItems={fetchItems}
          fetchProof={fetchProof}
          elements={
            flowData && flowData.states
              ? flowData.states.map((s) => s.name)
              : []
          }
          setLastEvent={setLastEvent}
        />
      ) : activePanel === "intent" ? (
        <InputContextProvider>
          <AbstractForm
            element={"intent"}
            fields={structure.intents || {}}
            flow={flow}
            elementData={
              flowData &&
              flowData.intents.filter((f) => f.name === activeElement)[0]
            }
            setLastEvent={setLastEvent}
            fetchProof={fetchProof}
            fetchItems={fetchItems}
            setActivePanel={setActivePanel}
            handleSubmit={convform}
          />
        </InputContextProvider>
      ) : activePanel === "list-intents" ? (
        <Listing
          elementType={"intent"}
          fields={structure.intents || {}}
          flow={flow}
          setActivePanel={setActivePanel}
          setActiveElement={setActiveElement}
          fetchItems={fetchItems}
          fetchProof={fetchProof}
          elements={
            flowData && flowData.intents
              ? flowData.intents.map((s) => s.name)
              : []
          }
          setLastEvent={setLastEvent}
        />
      ) : (
        <InputContextProvider>
          <AbstractForm
            element={"meta"}
            fields={structure.flow || {}}
            flow={flow}
            elementData={
              flowData &&
              Object.fromEntries(
                Object.entries(flowData).filter(
                  ([k]) => !["states", "intents"].includes(k),
                ),
              )
            }
            setLastEvent={setLastEvent}
            fetchProof={fetchProof}
            fetchItems={fetchItems}
            setActivePanel={setActivePanel}
            handleSubmit={convform}
          />
        </InputContextProvider>
      )}
    </div>
  );
};

EditorPanel.propTypes = {
  initial: PropTypes.string.isRequired,
  flow: PropTypes.string.isRequired,
  setLastEvent: PropTypes.func.isRequired,
  fetchProof: PropTypes.func.isRequired,
  flowData: PropTypes.object.isRequired,
  fetchItems: PropTypes.func.isRequired,
};

export default EditorPanel;
