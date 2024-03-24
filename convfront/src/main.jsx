import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from "./app/App.jsx";
import "./index.css";
import AdminConfig from "./admin/AdminConfig";
import { IssuesContextProvider } from "./IssuesContext";

const [bot, phase] = [window.bot, window.phase];

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route
          path="admin/*"
          element={
            <IssuesContextProvider>
              <AdminConfig />
            </IssuesContextProvider>
          }
        />
        <Route path="*" element={<App bot={bot} phase={phase} />} />
      </Routes>
    </Router>
  </React.StrictMode>,
);
