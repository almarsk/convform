import PropTypes from "prop-types";
import StringInput from "./input_types/StringInput";
import IntInput from "./input_types/IntInput";
import BoolInput from "./input_types/BoolInput";
import ListInput from "./input_types/ListInput";
import ResponseTypeInput from "./input_types/ResponseTypeInput";
import DictInput from "./input_types/DictInput";
import Say from "./input_types/Say";

const EditBrick = ({ label, type, activeItem, setChanges, setActiveItem }) => {
  return (
    <div className="editor-brick">
      <div className="editor-label">{label.replace(/_/g, " ")}</div>
      <div className="editor-field">
        {type === "str" ? (
          <StringInput
            activeItem={activeItem}
            label={label}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
          />
        ) : type === "int" ? (
          <IntInput
            activeItem={activeItem}
            label={label}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
          />
        ) : type === "bool" ? (
          <BoolInput
            activeItem={activeItem}
            label={label}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
          />
        ) : type === "list" ? (
          <ListInput
            activeItem={activeItem}
            label={label}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
          />
        ) : type === "ResponseType" ? (
          <ResponseTypeInput
            activeItem={activeItem}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
            label={label}
          />
        ) : type === "dict" ? (
          <DictInput
            activeItem={activeItem}
            label={label}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
          />
        ) : type.trim() === "list[tuple[convcore.say.Say, str]]" ? (
          <Say
            activeItem={activeItem}
            label={label}
            setActiveItem={setActiveItem}
            setChanges={setChanges}
          />
        ) : (
          `${type}`
        )}
      </div>
    </div>
  );
};

EditBrick.propTypes = {
  label: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default EditBrick;
