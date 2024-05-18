import PropTypes from "prop-types";

import slugify from "slugify";
import { useState } from "react";
import BotBrick from "./BotBrick";
import myRequest from "../myRequest";

const FlowList = ({ activeFlows, fetchBots, activeProject, setBotsList }) => {
  const [newFlowValue, setNewFlowValue] = useState("");

  const handleSubmitFlow = async (event) => {
    console.log(slugify(newFlowValue));
    event.preventDefault();
    setNewFlowValue("");
    await myRequest("/create", {
      item_type: "flow",
      name: slugify(newFlowValue),
      destination: activeProject,
    });
    setBotsList(await myRequest("/list-bots", {}));
  };

  return (
    <ul className="flow-list">
      {activeFlows.map(([botName, status, , project, a], i) => {
        return (
          <BotBrick
            key={i}
            bot={botName}
            status={status}
            archived={a}
            projectId={project}
            setBotsList={fetchBots}
          />
        );
      })}

      <div className="bot-brick">
        <form onSubmit={handleSubmitFlow}>
          <input
            required
            className="bot-name new-flow"
            placeholder="new flow"
            value={newFlowValue}
            onChange={(e) => setNewFlowValue(e.target.value)}
            type="text"
          />
          <button className="submit">↵</button>
        </form>
      </div>
    </ul>
  );
};

FlowList.propTypes = {
  activeFlows: PropTypes.arrayOf(PropTypes.array).isRequired,
  fetchBots: PropTypes.func.isRequired,
  activeProject: PropTypes.number.isRequired,
  setBotsList: PropTypes.func.isRequired,
};

export default FlowList;
