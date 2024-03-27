import { useState, useEffect } from "react";
import AdminPage from "./AdminPage";
import LoginPage from "./LoginPage";
import myRequest from "../myRequest";
import Flows from "./Flows";
import { Route, Routes } from "react-router-dom";
import EditPage from "./editor/EditPage";
import TestPage from "./TestPage";
import "./admin.scss";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";

const AdminConfig = () => {
  const { issues, setIssues } = useContext(IssuesContext);

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [unsuccess, setUnsuccess] = useState(false);

  const logOff = () => {
    setIsLoggedIn(false);
    localStorage.setItem("isLoggedIn", false);
    setIssues("");
  };

  const handleLogin = async (nick, pass) => {
    myRequest("/login", [nick, pass]).then((e) => {
      localStorage.setItem("isLoggedIn", e.success);
      setIsLoggedIn(e.success);
      setUnsuccess(!e.success);
    });
  };

  useEffect(() => {
    const loggedInStatus = localStorage.getItem("isLoggedIn");
    if (loggedInStatus == "true") {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <>
      {isLoggedIn ? (
        <AdminPage logOff={logOff}>
          <Routes>
            <Route index element={<Flows />} />
            <Route path="/edit/:flow" element={<EditPage />} />
            <Route path="/test/:flow" element={<TestPage />} />
          </Routes>
        </AdminPage>
      ) : (
        <LoginPage onLogin={handleLogin} unsuccess={unsuccess} />
      )}

      <div
        className="issues-summary"
        dangerouslySetInnerHTML={{
          __html: issues,
        }}
      />
    </>
  );
};

export default AdminConfig;
