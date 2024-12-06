import UserInput from "../app/UserInput";
import PropTypes from "prop-types";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const IntroExperiment = () => {
  return (
    <ul className="intro-text">
      <li className="center">
        Dobrý den,
        <br /> jmenuji se Albert Maršík a jsem studentem NMgr. oboru Empirická a
        komparativní lingvistika na FF UK.
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
        Pokud bude chatbot komunikovat nepřirozeně, konverzaci ukončete červeným
        tlačítkem.
      </li>
      <li>---</li>
      <li className="center">
        Po skočení konverzace vám bude zobrazen přepis celé konverzace.
        <br /> Prosím zaškrtněte promluvy chatbota, které se vám nelíbily, nebo
        vás nějak zaujaly a okomentujte je.
      </li>
      <li>---</li>
      <li className="center">
        {" "}
        <b>Upozornění</b>: Nevkládejte osobní informace.
      </li>
      <li>---</li>
      <b>Účastí na experimentu potvrzujete, že:</b>
      <ul>
        <li>
          a) jsem se seznámil/a s informacemi o cílech a průběhu výše popsaného
          výzkumu;
        </li>
        <li>b) dobrovolně souhlasím s účastí své osoby v tomto výzkumu;</li>
        <li>
          c) rozumím tomu, že se mohu kdykoli rozhodnout ve své účasti na
          výzkumu nepokračovat;
        </li>
        <li>
          d) jsem srozuměn s tím, že jakékoliv užití a zveřejnění dat a výstupů
          vzešlých z výzkumu nezakládá můj nárok na jakoukoliv odměnu či
          náhradu, tzn. že veškerá oprávnění k užití a zveřejnění dat a výstupů
          vzešlých z výzkumu poskytuji bezúplatně.
        </li>
        <li>---</li>
        <li>Zároveň prohlašuji, že</li>
      </ul>
      <ul>
        <li>
          a) souhlasím se zveřejněním anonymizovaných dat a výstupů vzešlých z
          výzkumu a s jejich dalším využitím;{" "}
        </li>

        <li>
          b) souhlasím se zpracováním a uchováním osobních a citlivých údajů v
          rozsahu v tomto informovaném souhlasu uvedených ze strany Univerzity
          Karlovy, Filozofické fakulty, IČ: 00216208, se sídlem: nám. Jana
          Palacha 2, 116 38 Praha 1, a to pro účely zpracování dat vzešlých z
          výzkumu, pro účely případného kontaktování z důvodu zpracování dat
          vzešlých z výzkumu či z důvodu nabídky účasti na obdobných akcích a
          pro účely evidence a archivace; a s tím, že tyto osobní údaje mohou
          být poskytnuty subjektům oprávněným k výkonu kontroly projektu, v
          jehož rámci výzkum realizován;{" "}
        </li>

        <li>
          c) jsem seznámen/-a se svými právy týkajícími se přístupu k informacím
          a jejich ochraně podle § 46 a § 49 zákona č. 110/2019 Sb., o ochraně
          osobních údajů a o změně některých zákonů, ve znění pozdějších
          předpisů, tedy že mohu požádat Univerzitu Karlovu v Praze o informaci
          o zpracování mých osobních a citlivých údajů a jsem oprávněn/-a ji
          dostat a že mohu požádat Univerzitu Karlovu v Praze o opravu
          nepřesných osobních údajů, doplnění osobních údajů, jejich blokaci a
          likvidaci.
        </li>
      </ul>
      <li>---</li>
      Výše uvedená svolení a souhlasy poskytuji dobrovolně na dobu neurčitou až
      do odvolání a zavazuji se je neodvolat bez závažného důvodu spočívajícího
      v podstatné změně okolností.
      <li>---</li>
      <li className="center">
        Pokud potřebujete splnit účast v experimentu v rámci LABELS, prosím
        uveďte svůj e-mail (stejný jako v registračním systému). Jinak uveďte
        libovolnou přezdívku:
      </li>
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
      <p className="centre">Díky, že se účastníte.</p>
    </ul>
  );
};

IntroExperiment.propTypes = {
  start: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
};

export default IntroExperiment;
