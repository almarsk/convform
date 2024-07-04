import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import myRequest from "../myRequest";
import basename from "../basename.jsx";

const Outro = () => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const comment = new FormData(e.target).get("comment");
    const grade = parseInt(new FormData(e.target).get("grade"));
    await myRequest("/outro", [comment, grade]).then(
      console.log(comment, grade),
      // () => (window.location.href = basename + "/"),
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
          <select name="grade" required className="submit">
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
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
