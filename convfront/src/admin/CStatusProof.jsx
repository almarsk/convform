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
    setMissing({
      states: [...cStatus.last_states, ...cStatus.context_states].filter(
        (s) => refs.states && !refs.states.includes(s),
      ),
      intents: [...cStatus.context_intents].filter(
        (i) => refs.intents && !refs.intents.includes(i),
      ),
    });
  }, [refs, cStatus]);

  return (
    <div className="cstatus-proof">
      <h4>Available</h4>
      <h5>intents:</h5>
      <div>{refs.intents && refs.intents.map((i) => `${i}, `)}</div>
      <h5>states:</h5>
      <div>{refs.states && refs.states.map((s) => `${s}, `)}</div>
      {missing &&
      Object.values(missing).every((i) => {
        return !i.length;
      }) ? (
        <h4>CStatus is valid.</h4>
      ) : (
        <>
          <h4>Missing</h4>
          {!!missing.intents.length && (
            <>
              <h5>intents:</h5>
              <div>{missing.intents.map((i) => `${i}, `)}</div>
            </>
          )}
          {!!missing.states.length && (
            <>
              <h5>states:</h5>
              <div>{missing.states.map((i) => `${i}, `)}</div>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default CStatusProof;
