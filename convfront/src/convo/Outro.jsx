import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import myRequest from "../myRequest";

const Outro = () => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const comment = new FormData(e.target).get("comment");
    const grade = new FormData(e.target).get("grade");
    await myRequest("/outro", [comment, grade]).then(
      () => (window.location.href = "/"),
    );
  };

  const [aborted, setAborted] = useState(false);

  useEffect(() => {
    const isAborted = async () => {
      return await myRequest("/is_aborted", {}).then((e) =>
        setAborted(e.aborted),
      );
    };
    isAborted();
  }, []);

  return (
    <form onSubmit={(e) => handleSubmit(e)}>
      <p className="content">
        {aborted
          ? "Proč jste konverzaci ukončili?"
          : "Jak konverzace proběhla?"}
        <br></br>Prosím ohodnoťte <b>slovně</b> a <b>známkou</b> jako ve škole:
      </p>
      <div className="outro-form">
        <textarea
          name="comment"
          className="eval-field input-field content"
          type="text"
          required
          placeholder="komentář"
        ></textarea>
        <div className="outro-eval">
          <input
            name="grade"
            required
            min="1"
            max="5"
            className="submit"
            type="number"
            inputMode="numeric"
            onKeyDown={(event) => event.preventDefault()}
          ></input>
          <button className="submit">↵</button>
        </div>
      </div>
    </form>
  );
};

Outro.propTypes = {
  submit: PropTypes.func.isRequired,
};

export default Outro;
