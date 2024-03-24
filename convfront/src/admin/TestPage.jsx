import { useEffect, useState } from "react";
import myRequest from "../myRequest";
import { Navigate, useParams } from "react-router-dom";

const states = {
  0: "valid",
  1: "invalid",
  2: "unknown",
};

const TestPage = () => {
  const { flow } = useParams();
  const [useValid, setValid] = useState(0);

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
      {states[useValid] == "unknown" ? <Navigate to="/" /> : ""}
      {states[useValid] == "invalid" ? <div>invalid flow, go fix</div> : ""}
    </div>
  );
};

export default TestPage;
