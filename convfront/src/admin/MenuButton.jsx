import PropTypes from "prop-types";
import { useContext } from "react";
import { Link } from "react-router-dom";
import { IssuesContext } from "../IssuesContext";

const MenuButton = ({ icon, click, hoverText, where }) => {
  const { setIssues } = useContext(IssuesContext);

  return (
    <Link
      className="submit admin-button"
      to={where}
      onMouseOver={() => {
        setIssues("");
        setIssues(hoverText.replace(/\n/g, "<br>"));
      }}
      onMouseLeave={() => setIssues("")}
      onClick={click}
    >
      {icon}️
    </Link>
  );
};

MenuButton.propTypes = {
  icon: PropTypes.node.isRequired,
  click: PropTypes.func.isRequired,
  hoverText: PropTypes.string.isRequired,
  where: PropTypes.string.isRequired,
};

export default MenuButton;
