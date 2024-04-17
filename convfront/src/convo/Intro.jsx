import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import basename from "../basename.jsx";
import { useState, useEffect } from "react";

const Intro = ({ bot }) => {
  const [instructions, setInstructions] = useState(null);
  useEffect(() => {
    const getInstructions = async () => {
      await myRequest("/instructions", {
        flow: bot,
      }).then((e) => {
        if (e.success) {
          setInstructions(e.message);
        } else {
          setInstructions(
            `Díky, že se účastníte vývoje chatbota jménem <i>${bot}</i>. Nejdřív prosím vyplňte libovolnou <b>přezdívku</b>:`,
          );
        }
      });
    };
    getInstructions();
  });

  return (
    <>
      <p id="intro-text">
        {" "}
        <span dangerouslySetInnerHTML={{ __html: instructions }}></span>
      </p>
      <UserInput
        submit={async (e) => {
          e.preventDefault();
          await myRequest("/intro", {
            nick: new FormData(e.target).get("content"),
          }).then(() => {
            window.location.href = basename + "/";
          });
        }}
        loading={false}
        display={[true, false]}
      />
    </>
  );
};

Intro.propTypes = {
  start: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
};

export default Intro;
