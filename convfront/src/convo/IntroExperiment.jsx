import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const IntroExperiment = () => {
  return (
    <>
      <p id="intro-text">
        Díky, že se účastníte. Nejdřív prosím vyplňte
        <b>přezdívku</b> <i>(tu stejnou co minule)</i>:
      </p>
      <UserInput
        submit={async (e) => {
          e.preventDefault();
          await myRequest("/intro_experiment", {
            nick: new FormData(e.target).get("content"),
          }).then((e) => {
            window.location.href =
              basename + `/route_experiment?username=${e.nick}`;
          });
        }}
        loading={false}
        display={[true, false]}
      />
    </>
  );
};

IntroExperiment.propTypes = {
  start: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
};

export default IntroExperiment;
