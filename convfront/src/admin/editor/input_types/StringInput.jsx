import PropTypes from "prop-types";

const StringInput = ({ label, activeItem, setChanges, setActiveItem }) => {
  return (
    <textarea
      className="input-field string-input"
      name={label}
      placeholder={label}
      value={activeItem && activeItem[label]}
      onChange={(e) => {
        setChanges(true);
        setActiveItem((prevActive) => {
          return { ...prevActive, [label]: e.target.value };
        });
      }}
    />
  );
};

StringInput.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default StringInput;
