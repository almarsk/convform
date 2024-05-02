import PropTypes from "prop-types";

import { useEffect, useRef } from "react";
import myRequest from "../../myRequest";
import slugify from "slugify";

const RenameItemForm = ({
  renameMode,
  setRenameMode,
  newItemValue,
  setNewItemValue,
  item,
  fetchProof,
  fetchItems,
  flow,
  setLastEvent,
  elementType,
}) => {
  const inputRef = useRef(null);
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.select();
      inputRef.current.focus();
    }
  }, [renameMode]);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        myRequest("/convform", {
          flow: flow,
          func: "rename",
          name: item,
          item_type: elementType,
          data: slugify(newItemValue),
        }).then((response) => {
          if (response.success) {
            fetchProof();
            fetchItems();
            setNewItemValue(slugify(newItemValue));
            setRenameMode(false);
            setLastEvent(
              `renamed ${elementType} from ${item} to ${newItemValue}`,
            );
          }
        });
      }}
      className="rename-flow-form project-name"
      style={{ width: "15px" }}
    >
      <input
        required
        ref={inputRef}
        className="new-flow"
        placeholder={`rename ${elementType}`}
        value={newItemValue}
        onChange={(e) => setNewItemValue(e.target.value)}
        type="text"
      />
    </form>
  );
};

RenameItemForm.propTypes = {
  renameMode: PropTypes.bool.isRequired,
  setRenameMode: PropTypes.func.isRequired,
  newItemValue: PropTypes.string.isRequired,
  setNewItemValue: PropTypes.func.isRequired,
  bot: PropTypes.string.isRequired,
  setBotsList: PropTypes.func.isRequired,
};

export default RenameItemForm;
