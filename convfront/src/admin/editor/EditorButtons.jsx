import PropTypes from "prop-types";
import MenuButton from "../MenuButton";

const EditorButtons = ({ setIssues, setActivePanel }) => {
  return (
    <div className="editor-menu">
      <MenuButton
        icon={"🎯"}
        hoverText={"state"}
        click={() => {
          setActivePanel("list-states");
        }}
      />
      <MenuButton
        icon={"💭"}
        hoverText={"intent"}
        click={() => setActivePanel("list-intents")}
      />
      <MenuButton
        icon={"🌎"}
        hoverText={"meta"}
        click={() => {
          setActivePanel("meta");
        }}
      />
    </div>
  );
};

EditorButtons.propTypes = {
  setActivePanel: PropTypes.func.isRequired,
};

export default EditorButtons;
