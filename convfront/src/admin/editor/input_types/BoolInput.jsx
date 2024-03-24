import PropTypes from "prop-types";

const BoolInput = ({ label, activeItem, setChanges, setActiveItem }) => {
  return (
    <div className="bool-input">
      <input
        type="checkbox"
        name={label}
        placeholder={label}
        checked={activeItem && activeItem[label]}
        onChange={(e) => {
          setChanges(true);
          setActiveItem((prevActive) => {
            return { ...prevActive, [label]: e.target.checked };
          });
        }}
      />
    </div>
  );
};

BoolInput.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default BoolInput;
