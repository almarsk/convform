import PropTypes from "prop-types";
import MenuButton from "./MenuButton";
import myRequest from "../myRequest";

const ProjectBrick = ({
  name,
  activeProject,
  id,
  setActiveProject,
  isArchived,
  archived,

  fetchProjects,
  isDefault,
}) => {
  return (
    <div
      /* eslint-disable-next-line react/no-unknown-property */
      project-id={id}
      className={`project-brick ${id == 0 ? "all-flows" : ""}`}
      onClick={() => setActiveProject(id)}
    >
      <span
        className={`project-name ${activeProject == id ? "bold-text" : ""}`}
      >
        {name}
      </span>
      {!isDefault ? (
        <MenuButton
          icon={isArchived ? "💡" : "💾"}
          click={async (e) => {
            e.stopPropagation();
            await myRequest("/move", {
              item_type: "project",
              name: name,
              destination: isArchived ? 1 : 2,
            }).then(() => {
              fetchProjects();
            });
          }}
          hoverText={`${archived ? "unarchive" : "archive"} project ${name}`}
        />
      ) : (
        ""
      )}
    </div>
  );
};

ProjectBrick.propTypes = {
  name: PropTypes.string.isRequired,
  activeProject: PropTypes.number.isRequired,
  id: PropTypes.number.isRequired,
  setActiveProject: PropTypes.func.isRequired,
  isArchived: PropTypes.bool.isRequired,
  archived: PropTypes.bool.isRequired,

  fetchProjects: PropTypes.func.isRequired,
  isDefault: PropTypes.bool.isRequired,
};

export default ProjectBrick;
