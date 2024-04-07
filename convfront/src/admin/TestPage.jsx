import { useEffect, useState } from "react";
import myRequest from "../myRequest";
import { Navigate, useParams, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";
import AbstractForm from "./editor/AbstractForm";
import CStatusReader from "./read/CStatusReader";
import CStatusProof from "./CStatusProof";

const states = {
  0: "valid",
  1: "invalid",
  2: "unknown",
};

const TestPage = () => {
  const { flow } = useParams();
  const [useValid, setValid] = useState(0);
  const navigate = useNavigate();
  const { cStatusStructure, testCStatus, setTestCStatus } =
    useContext(IssuesContext);
  const [result, setResult] = useState(null);
  const [activeCStatus, setActiveCStatus] = useState(null);

  useEffect(() => {
    myRequest("/proof", { flow: flow }).then((e) => {
      if (e.message === "invalid path") {
        setValid(2);
      } else if (!e.success) {
        setValid(1);
      }
    });

    const lc_cstatus = localStorage.getItem("testCStatus");
    !testCStatus &&
      lc_cstatus != "null" &&
      setTestCStatus(JSON.parse(lc_cstatus));
  }, []);

  return (
    <div className="test-page">
      <h4>testing {flow}</h4>
      <button className="submit" onClick={() => navigate(-1)}>
        ◀
      </button>
      {states[useValid] == "unknown" ? <Navigate to="/" /> : ""}
      {states[useValid] == "invalid" ? <div>invalid flow, go fix</div> : ""}
      {states[useValid] == "valid" ? (
        <div className="test-container">
          <div className="test-content">
            <CStatusProof cStatus={activeCStatus} flow={flow} />
          </div>
          <div className="test-content wide">
            <AbstractForm
              element={"cstatus in flow"}
              fields={
                cStatusStructure
                  ? // adding the user for the testing
                    // filtering our non descript fields for the testing
                    [...cStatusStructure, ["user_reply", "str"]].filter(
                      (i) => i[1] != "typing_extensions.Any",
                    )
                  : {}
              }
              flow={flow}
              elementData={cStatusData(
                testCStatus,
                cStatusStructure,
                testCStatus ? testCStatus.speech : "",
              )}
              handleSubmit={(result) => {
                console.log("active", result.activeItem);

                const newCStatus = async () =>
                  await myRequest("/bot", [
                    result.activeItem.user_reply,
                    result.activeItem,
                    0,
                    flow,
                  ]).then((e) => setResult(e));

                newCStatus();
                //setTestCStatus(result.activeItem);
              }}
              onChange={(item) => {
                setActiveCStatus(item);
              }}
            />
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
    : {};
}

function cStatusData(testCStatus, cStatusStructure, reply) {
  // adding the user reply for the testing
  const cStatusStructure_w_reply = cStatusStructure
    ? [...cStatusStructure, ["user_reply", "str"]]
    : cStatusStructure;
  const cstatus = testCStatus
    ? testCStatus.cstatus
    : templateCStatus(cStatusStructure_w_reply);
  cstatus["user_reply"] = reply;
  return cstatus;
}
