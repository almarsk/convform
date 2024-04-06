import { useEffect } from "react";
import myRequest from "../myRequest";
import { useState } from "react";

const CStatusProof = ({ cStatus, flow }) => {
  const [refs, setRefs] = useState({ states: [], intents: [] });
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
    console.log("les check");
    if (!cStatus) return;
    const toCheck = {
      last_states: { type: "states", content: cStatus.last_states },
      context_states: { type: "states", content: cStatus.context_states },
      context_intents: { type: "intents", content: cStatus.context_intents },
    };
    Object.entries(toCheck).forEach((cat) => {
      if ((!refs, cat[0])) setMissing((prev) => ({ ...prev, [cat]: [] }));
      console.log("lab", cat[0]);
      console.log("cat", cat[1]);
      cat[1].content.forEach((item) => {
        if (!refs[cat[1].type].includes(item))
          setMissing((prev) => ({ ...prev, [cat]: [...prev[cat], item] }));
      });
    });
  }, [refs, cStatus]);

  return <>{JSON.stringify(missing)}</>;
};

export default CStatusProof;
