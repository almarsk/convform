import myRequest from "../../myRequest";
import RenameItemForm from "./RenameItemForm";
import { useState } from "react";

const ItemBrick = ({
  itemName,
  elementType,
  flow,
  setActivePanel,
  setActiveElement,
  setLastEvent,
  fetchItems,
  fetchProof,
}) => {
  const [renameMode, setRenameMode] = useState(false);
  const [newItemValue, setNewItemValue] = useState(itemName);

  const removeButton = (e, elementName) => {
    e.stopPropagation();
    myRequest("/convform", {
      flow: flow,
      func: "remove",
      item_type: elementType,
      name: elementName,
    }).then(() => {
      fetchItems();
      fetchProof();
    });
  };

  const handleClick = (element) => {
    if (!renameMode) {
      setActivePanel(elementType);
      setActiveElement(element);
    }
  };

  return (
    <div onClick={() => handleClick(itemName)} className="project-brick">
      {renameMode ? (
        <RenameItemForm
          fetchItems={fetchItems}
          fetchProof={fetchProof}
          flow={flow}
          item={itemName}
          newItemValue={newItemValue}
          setRenameMode={setRenameMode}
          setNewItemValue={setNewItemValue}
          setLastEvent={setLastEvent}
          elementType={elementType}
        />
      ) : (
        <p className="project-name"> {itemName}</p>
      )}
      <div className="button-container">
        <button
          onClick={(e) => {
            e.stopPropagation();
            const copy_item = async () => {
              const really = window.confirm(`copy ${elementType} ${itemName}?`);
              really &&
                (await myRequest("/convform", {
                  flow: flow,
                  func: "copy",
                  name: itemName,
                  item_type: elementType,
                }).then(() => {
                  fetchProof();
                  fetchItems();
                  setLastEvent(`copied ${elementType} ${itemName}`);
                }));
            };
            copy_item();
          }}
          className="submit admin-button"
        >
          👥
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            setNewItemValue(itemName);
            setRenameMode((prev) => !prev);
          }}
          className="submit admin-button"
        >
          ✏️
        </button>
        <button
          onClick={(e) => {
            removeButton(e, itemName);
            setLastEvent(`removed ${elementType} ${itemName}`);
          }}
          className="submit admin-button"
        >
          ❌️
        </button>
      </div>
    </div>
  );
};

export default ItemBrick;
