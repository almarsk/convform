import myRequest from "../myRequest";
import basename from "../basename.jsx";
import { useState, useEffect } from "react";

const Start = ({ bot }) => {
  const [instructions, setInstructions] = useState(null);
  useEffect(() => {
    const getInstructions = async () => {
      await myRequest("/instructions", {
        flow: bot,
      }).then((e) => {
        if (e.success && e.message) {
          setInstructions(e.message);
        } else {
          setInstructions(
            "Můžeme začít. Pokud s vámi bude robot komunikovat nepřirozeně, ukončete ho červeným tlačítkem",
          );
        }
      });
    };
    getInstructions();
  });
  return (
    <>
      <p id="intro-text">
        <span
          dangerouslySetInnerHTML={{
            __html: instructions,
          }}
        ></span>
      </p>

      <form
        className="content-box"
        onSubmit={async (e) => {
          e.preventDefault();
          await myRequest("/start", {}).then(() => {
            window.location.href = basename + "/";
          });
        }}
      >
        <div className="content-box input">
          <button className="submit">↵</button>
        </div>
      </form>
    </>
  );
};

export default Start;
