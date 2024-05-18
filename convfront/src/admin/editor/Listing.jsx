import PropTypes from "prop-types";
import { useState } from "react";
import myRequest from "../../myRequest";
import ItemBrick from "./ItemBrick";
import slugify from "slugify";

const Listing = ({
  elementType,
  flow,
  fields,
  setActivePanel,
  setActiveElement,
  elements,
  fetchItems,
  fetchProof,
  setLastEvent,
}) => {
  const [newItemValue, setNewItemValue] = useState("");

  const handleSubmitItem = (e) => {
    e.preventDefault();
    console.log("new item value", slugify(newItemValue));
    const edit = async () => {
      const data = {};

      fields.forEach(([key, type]) => {
        data[key] =
          key == "name"
            ? slugify(newItemValue)
            : key == "initiativity"
              ? -1
              : determineDefault(type);
      });

      await myRequest("/convform", {
        flow: flow,
        func: "edit",
        item_type: elementType,
        name: newItemValue,
        data: data,
      }).then((e) => {
        fetchItems();
        fetchProof();
        e.success
          ? setLastEvent(`created ${elementType} ${newItemValue}`)
          : setLastEvent(`couldn't create ${elementType} ${newItemValue}`);
      });
    };
    edit();
    setNewItemValue("");
  };

  return (
    <div>
      <h5>{elementType}s</h5>
      <form
        className="project-brick new-project-form"
        onSubmit={handleSubmitItem}
      >
        <input
          required
          className="new-project"
          placeholder={`new ${elementType}`}
          value={newItemValue}
          onChange={(e) => setNewItemValue(e.target.value)}
          type="text"
        />
        <button className="submit admin-button">↵</button>
      </form>
      <ul className="items-list">
        {elements.map((f, i) => {
          return (
            <ItemBrick
              itemName={f}
              key={i}
              flow={flow}
              elementType={elementType}
              setActivePanel={setActivePanel}
              setActiveElement={setActiveElement}
              setLastEvent={setLastEvent}
              fetchItems={fetchItems}
              fetchProof={fetchProof}
            />
          );
        })}
      </ul>
    </div>
  );
};

Listing.propTypes = {
  elementType: PropTypes.string.isRequired,
  flow: PropTypes.string.isRequired,
  fields: PropTypes.array.isRequired,
  setActivePanel: PropTypes.func.isRequired,
  setActiveElement: PropTypes.func.isRequired,
  elements: PropTypes.array.isRequired,
  fetchItems: PropTypes.func.isRequired,
  fetchProof: PropTypes.func.isRequired,
  setLastEvent: PropTypes.func.isRequired,
};

export default Listing;

const determineDefault = (type) => {
  return type.includes("list")
    ? []
    : type.includes("dict")
      ? {}
      : type.includes("bool")
        ? false
        : type.includes("int")
          ? 1
          : type == "ResponseType"
            ? "responsive"
            : "";
};
