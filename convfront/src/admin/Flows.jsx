import PropTypes from "prop-types";

import { useState, useEffect } from "react";
import myRequest from "../myRequest";
import MenuButton from "./MenuButton";
import FlowList from "./FlowList";
import ProjectList from "./ProjectList";

const Flows = () => {
  const [botsList, setBotsList] = useState([]);
  const [projects, setProjectsList] = useState([]);
  const [archived, setArchived] = useState(false);

  const [activeProject, setActiveProject] = useState(1);
  const [activeFlows, setActiveFlows] = useState(botsList);

  const fetchProjects = async () => {
    try {
      const result = await myRequest("/list-projects", {});

      setProjectsList(result);
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  };

  const fetchBots = async () => {
    try {
      const result = await myRequest("/list-bots", {}).then((e) => {
        return e;
      });
      setBotsList(result);
    } catch (error) {
      console.error("Error fetching bots:", error);
    }
  };

  useEffect(() => {
    fetchBots();
    fetchProjects();
  }, []);

  useEffect(() => {
    if (activeProject === 0) {
      setActiveFlows(botsList);
    } else {
      const filteredFlows = botsList.filter(([, , , project_id]) => {
        return project_id === activeProject;
      });
      setActiveFlows(filteredFlows);
    }
  }, [activeProject, botsList]);

  return (
    <div className="listing_container">
      <div style={{ display: "flex", flexDirection: "row" }}>
        <MenuButton
          icon={archived ? "📂" : "📁"}
          click={() => {
            setArchived((prevArchived) => !prevArchived);
          }}
          hoverText={`${archived ? "hide" : "view"} archived`}
        />
        {archived ? (
          <MenuButton
            icon={"❌"}
            click={async () => {
              await myRequest("/stash", {}).then((e) => {
                fetchBots();
                fetchProjects();
              });
            }}
            hoverText={`remove archived`}
          />
        ) : (
          ""
        )}
      </div>
      <div className="flow-container">
        <ProjectList
          archived={archived}
          setProjectsList={setProjectsList}
          projects={projects}
          setActiveProject={setActiveProject}
          activeProject={activeProject}
          fetchProjects={fetchProjects}
        />

        <FlowList
          activeFlows={activeFlows}
          fetchBots={fetchBots}
          activeProject={activeProject}
          setBotsList={setBotsList}
        />
      </div>
    </div>
  );
};

Flows.propTypes = {};

export default Flows;
