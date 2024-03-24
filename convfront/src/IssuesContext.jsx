import { createContext, useState } from "react";
import PropTypes from "prop-types";

const IssuesContext = createContext();

const IssuesContextProvider = ({ children }) => {
  const [issues, setIssues] = useState("");

  return (
    <IssuesContext.Provider value={{ issues, setIssues }}>
      {children}
    </IssuesContext.Provider>
  );
};

IssuesContextProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export { IssuesContext, IssuesContextProvider };
