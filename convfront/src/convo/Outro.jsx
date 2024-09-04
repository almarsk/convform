import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import LogRater from "./log-rater/LogRater.jsx";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const Outro = () => {
  const [convo, setConvo] = useState([]);
  const [rating, setRating] = useState(3);

  const handleSubmit = async () => {
    await myRequest("/outro", [rating, convo]).then(
      () => (window.location.href = basename + "/"),
    );
  };

  useEffect(() => {
    const getConvo = async () => {
      const convo_for_annotation = await myRequest("/convo");
      setConvo(convo_for_annotation);
    };
    getConvo();
  }, []);

  return (
    <>
      <form className="outro-form-parent">
        <div className="outro-eval">
          <span className="log-rater-turn">
            Ohodnoťte přirozenost konverzace jako <b>ve škole</b>:
          </span>
          <select
            name="grade"
            value={rating}
            required
            className="submit"
            onChange={(e) => {
              setRating(e.target.value);
            }}
          >
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
        </div>
        <LogRater
          convo={convo.convo || []}
          setConvo={(updatedConvo) => {
            setConvo({ ...convo, convo: updatedConvo });
          }}
        />
        <div className="submit-panel">
          <button
            onClick={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
            className="submit submit-outro"
          >
            ↵
          </button>
        </div>
      </form>
    </>
  );
};

Outro.propTypes = {
  submit: PropTypes.func.isRequired,
};

export default Outro;
