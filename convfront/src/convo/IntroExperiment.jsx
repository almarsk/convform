import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const IntroExperiment = () => {
  return (
    <>
      <ul id="intro-text">
        <li className="center">
          Dobrý den,
          <br /> jmenuji se Albert Maršík a jsem studentem NMgr. oboru Empirická
          a komparativní lingvistika na FF UK.
        </li>
        <li className="center">V rámci studia se věnuji výzkumu konverzace.</li>
        <li className="center">
          Pro svou diplomovou práci jsem připravil chatbota, program, který si s
          vámi bude povídat.
          <br /> Povídejte si s ním, jak je vám přirozené.
          <br /> Téma konverzace není předem určeno a záleží do značené míry na
          vás.
        </li>
        <li>---</li>
        <li className="center">
          Během experimentu uvidíte vždy poslední promluvu chatbota a políčko na
          vepsaní vaší další odpovědi.
        </li>
        <li className="center">
          Konverzace bude trvat několik minut a chatbot se poté sám rozloučí.
        </li>
        <li className="center">
          Pokud bude chatbot komunikovat nepřirozeně, konverzaci ukončete
          červeným tlačítkem.
        </li>
        <li>---</li>
        <li className="center">
          Po skočení konverzace vám bude zobrazen přepis celé konverzace.
          <br /> Prosím zaškrtněte promluvy chatbota, které se vám nelíbily,
          nebo vás nějak zaujaly a okomentujte je.
        </li>
        <li>---</li>
        <li className="center">
          {" "}
          <b>Upozornění</b>: Nevkládejte osobní informace.
        </li>
        <li className="centre">Díky, že se účastníte.</li>
        <li className="center">
          Nejdřív prosím vyplňte <b>identifikační číslo</b>, které jste obdrželi
          v emailu:
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
    </>
  );
};

IntroExperiment.propTypes = {
  start: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
};

export default IntroExperiment;
