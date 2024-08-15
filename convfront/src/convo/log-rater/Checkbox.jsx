import PropTypes from "prop-types";

const CheckBox = ({ checked, onCheck }) => {
  return <input type="checkbox" onClick={onCheck} />;
};

CheckBox.propTypes = {
  checked: PropTypes.bool.isRequired,
  onCheck: PropTypes.func.isRequired,
};

export default CheckBox;
