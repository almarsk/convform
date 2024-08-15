import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import LogRater from "./log-rater/LogRater.jsx";
import myRequest from "../myRequest";
import basename from "../basename.jsx";
import Question from "./log-rater/Question.jsx";

import mockConvo from "./log-rater/mock-convo.js";

const Outro = () => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const comment = new FormData(e.target).get("comment");
    const grade = new FormData(e.target).get("grade");
    await myRequest("/outro", [comment, grade]).then(
      () => (window.location.href = basename + "/"),
    );
  };

  const [aborted, setAborted] = useState(false);
  const [convo, setConvo] = useState(mockConvo);

  useEffect(() => {
    const isAborted = async () => {
      return await myRequest("/is_aborted", {}).then((e) =>
        setAborted(e.aborted),
      );
    };
    isAborted();
  }, []);

  return (
    <>
      <form onSubmit={(e) => handleSubmit(e)} className="outro-form-parent">
        <Question
          evaluate={true}
          text={
            <p className="content">
              {aborted
                ? "Proč jste konverzaci ukončili?"
                : "Jak konverzace proběhla?"}
              <br></br>Prosím ohodnoťte <b>slovně</b> a <b>známkou</b> jako ve
              škole:
            </p>
          }
          setConvo={(updatedQ) =>
            setConvo({
              ...convo,
              questions: convo.questions.map((q, i) =>
                i == 0 ? { ...updatedQ } : { ...q },
              ),
            })
          }
          comment={convo.questions[0].comment}
          evaluation={convo.questions[0].rating}
        />
        <Question
          evaluate={false}
          text={
            <p className="content">
              Měli jste někdy chuť konverzaci <b>ukončit</b>? Kdy?
            </p>
          }
          setConvo={(updatedQ) =>
            setConvo({
              ...convo,
              questions: convo.questions.map((q, i) => {
                i == 1 ? { ...updatedQ } : { ...q };
              }),
            })
          }
          comment={convo.questions[1].comment}
          evaluation={convo.questions[1].rating}
        />

        <LogRater
          convo={convo.convo}
          setConvo={(updatedConvo) => {
            setConvo({ ...convo, convo: updatedConvo });
          }}
        />
        <div className="submit-panel">
          <button
            onClick={() => {
              console.log(convo);
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
