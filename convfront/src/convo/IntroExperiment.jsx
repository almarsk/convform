import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const IntroExperiment = () => {
  return (
    <>
      <ul id="intro-text">
        <li>Díky, že se účastníte.</li>
        <li>––</li>
        <li>Budete si povídat s chatbotem. </li>
        <li>Povídejte si s ním, jak je vám přirozené.</li>
        <li>––</li>
        <li>
          Konverzace bude trvat několik minut a chatbot se poté sám rozloučí.
        </li>
        <li>
          Pokud bude chatbot komunikovat nepřirozeně, konverzaci ukončete
          červeným tlačítkem.
        </li>
        <li>––</li>
        <li>
          Nejdřív prosím vyplňte <b>přezdívku</b>{" "}
          <i>(kdyžtak tu stejnou co minule)</i>:
        </li>
      </ul>
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
      <ul>
        <li className="center">
          <b>Upozornění:</b> Nevkládejte osobní informace.
        </li>
        <li className="center">Na konci prosím vyplňte dotazník.</li>
        <li className="center">Na mobilu nejlépe horizontálně.</li>
      </ul>
    </>
  );
};

IntroExperiment.propTypes = {
  start: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
};

export default IntroExperiment;
