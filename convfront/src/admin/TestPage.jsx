import { useEffect, useState } from "react";
import myRequest from "../myRequest";
import { Navigate, useParams, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";
import AbstractForm from "./editor/AbstractForm";

const states = {
  0: "valid",
  1: "invalid",
  2: "unknown",
};

const TestPage = () => {
  const { flow } = useParams();
  const [useValid, setValid] = useState(0);
  const { testCStatus } = useContext(IssuesContext);
  const navigate = useNavigate();
  const { setIssues, cStatusStructure } = useContext(IssuesContext);

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

    console.log("structure", cStatusStructure);
  }, []);

  return (
    <div>
      <h2>Test Page</h2>
      <div>{flow}</div>
      <button
        className="submit"
        onClick={() => navigate(-1)}
        onMouseOver={() => {
          setIssues("");
          setIssues("back to conversation log");
        }}
        onMouseLeave={() => setIssues("")}
      >
        ◀
      </button>
      {states[useValid] == "unknown" ? <Navigate to="/" /> : ""}
      {states[useValid] == "invalid" ? <div>invalid flow, go fix</div> : ""}
      {states[useValid] == "valid" ? (
        <div>
          <AbstractForm
            element={"cstatus in flow"}
            fields={
              cStatusStructure
                ? cStatusStructure.filter(
                    (i) => i[1] != "typing_extensions.Any",
                  )
                : {}
            }
            flow={flow}
            elementData={{}}
            //fetchItems={fetchItems}
          />
        </div>
      ) : (
        ""
      )}
    </div>
  );
};

export default TestPage;
