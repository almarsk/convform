import PropTypes from "prop-types";

const Question = ({ evaluate, text, comment, evaluation, setConvo }) => {
  return (
    <>
      {text}
      <div className="outro-form">
        <textarea
          className="eval-field input-field content"
          type="text"
          required
          placeholder="odpověď"
          value={comment}
          onChange={(e) => setConvo(e.target.value)}
        ></textarea>
        {evaluate && (
          <div className="outro-eval">
            <select
              name="grade"
              required
              className="submit"
              value={evaluation}
              onChange={setConvo}
            >
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </div>
        )}
      </div>
    </>
  );
};

Question.propTypes = {
  evaluate: PropTypes.bool.isRequired,
};

export default Question;
