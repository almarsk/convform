import { useEffect } from "react";
import PropTypes from "prop-types";
import { Link, useLocation } from "react-router-dom";

import MenuButton from "./MenuButton";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";

const AdminPage = ({ logOff, children, propValue }) => {
  const location = useLocation();
  const { setIssues } = useContext(IssuesContext);

  useEffect(() => {
    setIssues("");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location]);

  return (
    <div className="admin-container">
      <Link className="title" to="/admin">
        <h1 className="admin-header">Admin</h1>
      </Link>
      {children}
      <div className="log-off">
        <MenuButton icon={"👋"} hoverText={"log off"} click={logOff} />
      </div>
      <div>{propValue}</div>
    </div>
  );
};

AdminPage.propTypes = {
  logOff: PropTypes.func.isRequired,
  children: PropTypes.node,
  propValue: PropTypes.any.isRequired,
};

export default AdminPage;
