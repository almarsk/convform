import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const Intro = ({ bot }) => {
  return (
    <div className="box">
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
            window.location.href = basename + "/";
          });
        }}
        loading={false}
        display={[true, false]}
      />
      <p className="center">Upozornění: nevkládejte osobní informace</p>
      <p className="center">Prosba: na konci prosím vyplňte dotazník</p>
      <p className="center">Doporučení: na mobilu nejlépe horizontálně</p>
    </div>
  );
};

Intro.propTypes = {
  start: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
};

export default Intro;
