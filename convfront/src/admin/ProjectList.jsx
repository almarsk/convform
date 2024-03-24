import { useState } from "react";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import ProjectBrick from "./ProjectBrick";

const ProjectList = ({
  setProjectsList,
  archived,
  projects,
  setActiveProject,
  activeProject,
  setIssues,
  fetchProjects,
}) => {
  const [newProjectValue, setNewProjectValue] = useState("");

  const handleSubmitProject = async (event) => {
    event.preventDefault();
    setNewProjectValue("");
    await myRequest("/create", {
      item_type: "project",
      name: newProjectValue,
      destination: activeProject,
    });
    setProjectsList(await myRequest("/list-projects", {}));
  };

  return (
    <>
      <div className="project-container">
        <ul className="project-list">
          {projects
            .filter(([id, , , isArchived]) =>
              archived ? true : !isArchived && id != 2,
            )
            .map(([id, name, , isArchived, isDefault], index) => {
              return (
                <ProjectBrick
                  key={index}
                  name={name}
                  activeProject={activeProject}
                  id={id}
                  setActiveProject={setActiveProject}
                  isArchived={isArchived}
                  archived={archived}
                  fetchProjects={fetchProjects}
                  isDefault={isDefault}
                />
              );
            })}
          <ProjectBrick
            name="all"
            activeProject={activeProject}
            id={0}
            setActiveProject={setActiveProject}
            isArchived={false}
            archived={archived}
            fetchProjects={fetchProjects}
            isDefault={true}
          />

          <form
            className="project-brick new-project-form"
            onSubmit={handleSubmitProject}
          >
            <input
              required
              className="new-project"
              placeholder="new project"
              value={newProjectValue}
              onChange={(e) => setNewProjectValue(e.target.value)}
              type="text"
            />
            <button className="submit admin-button">↵</button>
          </form>
        </ul>
      </div>
    </>
  );
};

ProjectList.propTypes = {
  setProjectsList: PropTypes.func.isRequired,
  archived: PropTypes.bool.isRequired,
  projects: PropTypes.arrayOf(
    PropTypes.arrayOf(
      PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    ),
  ).isRequired,
  setActiveProject: PropTypes.func.isRequired,
  activeProject: PropTypes.number.isRequired,

  fetchProjects: PropTypes.func.isRequired,
};

export default ProjectList;
