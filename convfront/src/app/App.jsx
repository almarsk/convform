import "./App.css";
import PropTypes from "prop-types";
import Intro from "../convo/Intro";
import Chat from "../convo/Chat";
import Outro from "../convo/Outro";
import Start from "../convo/Start";
import { Link } from "react-router-dom";

const PHASES = {
  INTRO: 0,
  START: 1,
  CHAT: 2,
  OUTRO: 3,
};

const App = ({ bot, phase }) => {
  phase = parseInt(phase);
  console.log(phase);

  return (
    <div id="main">
      {localStorage.getItem("isLoggedIn") == "true" ? (
        <div className="log-off">
          <Link className="submit admin-button" to="/admin">
            🏠
          </Link>
        </div>
      ) : (
        ""
      )}

      {bot ? (
        phase === PHASES.INTRO ? (
          <Intro bot={bot} />
        ) : phase === PHASES.START ? (
          <Start />
        ) : phase === PHASES.CHAT ? (
          <Chat />
        ) : phase === PHASES.OUTRO ? (
          <Outro />
        ) : (
          <div>Díky za váš čas!</div>
        )
      ) : (
        <div>🤖🤒</div>
      )}
    </div>
  );
};

App.propTypes = {
  bot: PropTypes.string.isRequired,
  phase: PropTypes.number.isRequired,
};

export default App;
