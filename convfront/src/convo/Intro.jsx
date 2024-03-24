import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import { Navigate } from "react-router-dom";

const Intro = ({ bot }) => {
  return (
    <>
      <p id="intro-text">
        Díky, že se účastníte vývoje chatbota jménem <i>{bot}</i>. Nejdřív
        prosím vyplňte libovolnou <b>přezdívku</b>:
      </p>
      <UserInput
        submit={async (e) => {
          e.preventDefault();
          await myRequest("/intro", {
            nick: new FormData(e.target).get("content"),
          }).then(() => {
            <Navigate to="/" />;
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
