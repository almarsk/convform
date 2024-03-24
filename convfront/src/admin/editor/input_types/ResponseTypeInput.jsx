import PropTypes from "prop-types";

const ResponseTypeInput = ({
  label,
  activeItem,
  setChanges,
  setActiveItem,
}) => {
  const handleSelect = (e) => {
    setChanges(true);
    setActiveItem((prev) => {
      return { ...prev, [label]: e.target.value };
    });
  };

  return (
    <div className="response-type-input">
      <select
        value={activeItem && activeItem[label]}
        className="input-field"
        id="qualities"
        onChange={handleSelect}
      >
        <option value="initiative">Initiative</option>
        <option value="responsive">Responsive</option>
        <option value="flexible">Flexible</option>
        <option value="connective">Connective</option>
      </select>
    </div>
  );
};

ResponseTypeInput.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default ResponseTypeInput;
