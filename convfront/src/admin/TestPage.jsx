import { useEffect, useState } from "react";
import myRequest from "../myRequest";
import { Navigate, useParams, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";

const states = {
  0: "valid",
  1: "invalid",
  2: "unknown",
};

const TestPage = () => {
  const { flow } = useParams();
  const [useValid, setValid] = useState(0);
  const { setIssues, testCStatus } = useContext(IssuesContext);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("test", testCStatus);
  }, []);

  useEffect(() => {
    myRequest("/proof", { flow: flow }).then((e) => {
      if (e.message === "invalid path") {
        setValid(2);
      } else if (!e.success) {
        setValid(1);
      }
    });
  }, []);

  return (
    <div>
      <h2>Test Page</h2>
      <div>{flow}</div>
      <button className="submit" onClick={() => navigate(-1)}>
        ◀
      </button>
      {states[useValid] == "unknown" ? <Navigate to="/" /> : ""}
      {states[useValid] == "invalid" ? <div>invalid flow, go fix</div> : ""}
    </div>
  );
};

export default TestPage;
