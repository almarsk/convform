import PropTypes from "prop-types";

const IntInput = ({ label, activeItem, setChanges, setActiveItem, narrow }) => {
  return (
    <input
      min={-1}
      type="number"
      className={`input-field ${narrow && "narrow"}`}
      name={label}
      placeholder={label}
      value={activeItem && activeItem[label]}
      onChange={(e) => {
        setChanges(true);
        setActiveItem((prevActive) => {
          return { ...prevActive, [label]: parseInt(e.target.value) };
        });
      }}
    />
  );
};

IntInput.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default IntInput;
