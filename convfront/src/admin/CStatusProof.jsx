import { useEffect } from "react";
import myRequest from "../myRequest";
import { useState } from "react";

const CStatusProof = ({ cStatus, flow }) => {
  const [refs, setRefs] = useState({});
  const [missing, setMissing] = useState({});

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
    if (!cStatus || !refs) return;
    const toCheck = {
      last_states: { type: "states", content: cStatus.last_states || [] },
      context_states: { type: "states", content: cStatus.context_states || [] },
      context_intents: {
        type: "intents",
        content: cStatus.context_intents || [],
      },
    };

    const m = setMissing(
      Object.entries(toCheck).reduce((acc, [, { type, content }]) => {
        if (!acc[type]) acc[type] = [];
        acc[type] = [...acc[type], content].filter(
          (item) => refs[type] && !refs[type].includes(item),
        );
        return acc;
      }, {}),
    );

    console.log("miss", m);

    Object.entries(toCheck).forEach((cat) => {
      if (!refs[cat[1].type])
        setMissing((prev) => ({ ...prev, [cat[1].type]: [] }));
      cat[1].content.forEach((item) => {
        if (
          refs[cat[1].type] &&
          !refs[cat[1].type].includes(item) &&
          !missing[cat[1].type].includes(item)
        ) {
          console.log(refs);
          console.log(item);
          setMissing((prev) => ({
            ...prev,
            [cat[1].type]: [...prev[cat[1].type], item],
          }));
        }
      });
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
