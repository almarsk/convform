import { useEffect } from "react";
import myRequest from "../myRequest";

const Thanks = () => {
  useEffect(() => {
    const reset = async () => {
      await myRequest("/reset", {});
    };
    reset();
  });

  return <div>Díky za váš čas!</div>;
};

export default Thanks;
