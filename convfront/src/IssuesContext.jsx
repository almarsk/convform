import { createContext, useState } from "react";
import PropTypes from "prop-types";
import myRequest from "./myRequest";
import { useEffect } from "react";

const IssuesContext = createContext();

const IssuesContextProvider = ({ children }) => {
  const [issues, setIssues] = useState("");
  const [testCStatus, setTestCStatus] = useState(null);
  const [cStatusStructure, setCStatusStructure] = useState(null);

  useEffect(() => {
    myRequest("/structure").then((e) => {
      setCStatusStructure(e.cstatus);
    });
  }, []);

  return (
    <IssuesContext.Provider
      value={{
        issues,
        setIssues,
        testCStatus,
        setTestCStatus,
        cStatusStructure,
      }}
    >
      {children}
    </IssuesContext.Provider>
  );
};

IssuesContextProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export { IssuesContext, IssuesContextProvider };
