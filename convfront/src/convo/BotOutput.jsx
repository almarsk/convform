import PropTypes from "prop-types";

const BotOutput = ({ botSpeech, loading }) => {
  return (
    <div className="content-box">
      <p className="icon">🤖:️</p>
      {loading ? (
        <div className="loader"></div>
      ) : (
        <div className="content">{botSpeech}</div>
      )}
    </div>
  );
};

BotOutput.propTypes = {
  botSpeech: PropTypes.string.isRequired,
  loading: PropTypes.bool.isRequired,
};

export default BotOutput;
