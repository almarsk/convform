import { useState } from "react";
import PropTypes from "prop-types";

const NewItem = ({ addTag, label, area }) => {
  const [newValue, setNewValue] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        newValue && addTag(newValue);
        setNewValue("");
      }}
      className="list-field"
    >
      {!area ? (
        <input
          className="list-input single-line"
          onChange={(e) => setNewValue(e.target.value)}
          value={newValue}
          placeholder={label}
        />
      ) : (
        <div>
          <textarea
            className="area-input"
            onChange={(e) => setNewValue(e.target.value)}
            value={newValue}
            placeholder={label}
          />
          <button className="prompt-button prompt-submit">
            <div>↵</div>
          </button>
        </div>
      )}
    </form>
  );
};

NewItem.propTypes = {
  addTag: PropTypes.func.isRequired,
  label: PropTypes.string.isRequired,
  area: PropTypes.bool,
};

export default NewItem;
