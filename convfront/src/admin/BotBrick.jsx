import PropTypes from "prop-types";

import MenuButton from "./MenuButton";
import myRequest from "../myRequest";
import { useState } from "react";
import DraggableLabel from "./DraggableLabel";
import RenameFlowForm from "./RenameFlowForm";
import download_flow from "./download_flow";

import basename from "../basename.jsx";

const BotBrick = ({ bot, status, archived, setBotsList }) => {
  const [renameMode, setRenameMode] = useState(false);
  const [newFlowValue, setNewFlowValue] = useState(bot);

  return (
    <div className="bot-brick">
      <div className="bot-name">
        {!renameMode ? (
          <DraggableLabel
            bot={bot}
            statusSuccess={status.success}
            setBotsList={setBotsList}
          />
        ) : (
          <RenameFlowForm
            renameMode={renameMode}
            setRenameMode={setRenameMode}
            newFlowValue={newFlowValue}
            setNewFlowValue={setNewFlowValue}
            bot={bot}
            setBotsList={setBotsList}
          />
        )}
      </div>

      <div
        style={{
          opacity: status.success ? 100 : 0,
          zIndex: status.success ? 10 : -1,
        }}
      >
        <MenuButton
          icon={"🚀"}
          hoverText={`redirect to ${bot}`}
          click={() => {
            if (status.success)
              window.open(`${basename}/?flow=${bot}`, "_blank");
          }}
        />
      </div>

      <MenuButton
        icon={"📎"}
        hoverText={`link for ${bot}`}
        click={() => {
          const flow_url = `${new URL(window.location.href).origin}${basename}/?flow=${bot.normalize("NFD").replace(/[\u0300-\u036f]/g, "")}`;
          navigator.clipboard.writeText(flow_url);
        }}
      />

      <MenuButton
        icon={"✏️"}
        hoverText={`change name of ${bot}`}
        click={() => {
          setRenameMode((prev) => !prev);
          setNewFlowValue(bot);
        }}
      />

      <MenuButton
        icon={"🔍"}
        hoverText={`test ${bot}`}
        where={`/admin/test/${bot}`}
      />

      <MenuButton
        icon={"📖"}
        hoverText={`read conversations of ${bot}`}
        where={`/admin/read/${bot}`}
      />

      <MenuButton
        icon={status.success ? "🏗️" : "🛠️"}
        hoverText={status.message}
        where={`/admin/edit/${bot}`}
      />

      <MenuButton
        icon={"👥"}
        hoverText={`create copy of ${bot}`}
        click={async () => {
          const really = window.confirm(`copy flow ${bot}?`);
          really &&
            (await myRequest("/copy_flow", { name: bot }).then(() =>
              setBotsList(),
            ));
        }}
      />

      <MenuButton
        icon={"📥️"}
        hoverText={`export ${bot} in json`}
        click={() => download_flow(bot)}
      />

      <MenuButton
        icon={archived ? "💡" : "💾"}
        hoverText={"archive bot"}
        click={() => {
          myRequest("/move", {
            item_type: "flow",
            name: bot,
            destination: archived ? 1 : 2,
          }).then(() => setBotsList());
        }}
      />
    </div>
  );
};

BotBrick.propTypes = {
  bot: PropTypes.string.isRequired,
  status: PropTypes.shape({
    success: PropTypes.bool.isRequired,
    message: PropTypes.string.isRequired,
  }).isRequired,
  archived: PropTypes.bool.isRequired,
  setBotsList: PropTypes.func.isRequired,
};

export default BotBrick;
