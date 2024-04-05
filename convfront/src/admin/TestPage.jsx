import { useEffect, useState } from "react";
import myRequest from "../myRequest";
import { Navigate, useParams, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";
import AbstractForm from "./editor/AbstractForm";
import CStatusReader from "./read/CStatusReader";
import StringInput from "./editor/input_types/StringInput";

const states = {
  0: "valid",
  1: "invalid",
  2: "unknown",
};

const TestPage = () => {
  const { flow } = useParams();
  const [useValid, setValid] = useState(0);
  const navigate = useNavigate();
  const { cStatusStructure, testCStatus } = useContext(IssuesContext);
  const [result, setResult] = useState(null);
  const [say, setSay] = useState("");

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
    <div className="test-page">
      <h5>testing {flow}</h5>
      <button className="submit" onClick={() => navigate(-1)}>
        ◀
      </button>
      {states[useValid] == "unknown" ? <Navigate to="/" /> : ""}
      {states[useValid] == "invalid" ? <div>invalid flow, go fix</div> : ""}
      {states[useValid] == "valid" ? (
        <div className="test-container">
          <div className="test-content"></div>
          <div className="test-content wide">
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
              elementData={
                testCStatus
                  ? testCStatus.cstatus
                  : templateCStatus(cStatusStructure)
              }
              handleSubmit={(result) => {
                setResult(result.activeItem);
              }}
            />
            <div className="test-submit">
              <StringInput label="user turn" />
              <button className="submit cell">🚀</button>
            </div>
          </div>
          <div className="test-content">
            {result && (
              <CStatusReader
                cStatusStructure={cStatusStructure}
                turn={{ cstatus: result }}
              />
            )}
          </div>
        </div>
      ) : (
        ""
      )}
    </div>
  );
};

export default TestPage;

function templateCStatus(cStatusStructure) {
  return cStatusStructure
    ? cStatusStructure.reduce((empty, [key, itemType]) => {
        empty[key] =
          itemType == "list"
            ? []
            : itemType == "dict"
              ? {}
              : itemType == "int"
                ? 0
                : "";
        return empty;
      }, {})
    : null;
}
