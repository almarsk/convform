import PropTypes from "prop-types";
import { useState } from "react";

const UserInput = ({ submit, loading }) => {
  const [inputValue, setInputValue] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    setInputValue("");
    submit(event);
  };

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };
  return (
    <form className="content-box input" onSubmit={handleSubmit}>
      <p className="icon">🗣:️</p>
      <input
        required
        className="input-field-chat content"
        name="content"
        onChange={handleChange}
        type="text"
        value={inputValue}
      ></input>

      <button
        style={{
          zIndex: loading ? -1 : 1,
        }}
        className="submit"
      >
        ↵
      </button>
    </form>
  );
};

UserInput.propTypes = {
  submit: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
};

export default UserInput;
