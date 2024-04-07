import { useEffect } from "react";
import myRequest from "../myRequest";
import { useState } from "react";

const CStatusProof = ({ cStatus, flow, missing, setMissing }) => {
  const [refs, setRefs] = useState({});

  useEffect(() => {
    const get_flow = async () => {
      await myRequest("/export_flow", { name: flow }).then((e) => {
        setRefs({
          states: e.flow.states.map((s) => s.name),
          intents: e.flow.intents.map((i) => i.name),
        });
      });
    };
    get_flow();
  }, []);

  useEffect(() => {
    if (!cStatus || !cStatus.last_states || !refs) return;
    console.log("cs!", cStatus);
    setMissing({
      states: [...cStatus.last_states, ...cStatus.context_states].filter(
        (s) => refs.states && !refs.states.includes(s),
      ),
      intents: [...cStatus.context_intents].filter(
        (i) => refs.intents && !refs.intents.includes(i),
      ),
    });
  }, [refs, cStatus]);

  useEffect(() => {
    console.log("r", refs);
    console.log("m", missing);
  }, [missing]);
  useEffect(() => {
    console.log("c", cStatus);
  }, [cStatus]);

  return (
    <div className="cstatus-proof">
      <h4>available</h4>
      <h5>intents:</h5>
      <div>{refs.intents && refs.intents.map((i) => `${i} `)}</div>
      <h5>states:</h5>
      <div>{refs.states && refs.states.map((s) => `${s} `)}</div>
      {missing && Object.values(missing).some((value) => !!value) ? (
        <>
          <h4>missing</h4>
          <h5>intents:</h5>
          <div>{missing.intents && missing.intents.map((i) => `${i} `)}</div>
          <h5>states:</h5>{" "}
          <div>{missing.states && missing.states.map((s) => `${s} `)}</div>
        </>
      ) : (
        ""
      )}
    </div>
  );
};

export default CStatusProof;
