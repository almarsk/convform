import PropTypes from "prop-types";

const Counter = ({ label, activeItem, setChanges, setActiveItem }) => {
  console.log(activeItem[label]);

  return <input />;
};

Counter.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default Counter;
