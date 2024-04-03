import { useEffect, useState } from "react";

import myRequest from "../../myRequest";
import PropTypes from "prop-types";
import EditBrick from "./EditBrick";

const AbstractForm = ({
  element,
  elementData,
  fields,
  flow,
  setLastEvent,
  fetchProof,
  fetchItems,
}) => {
  const [, setChanges] = useState(false);
  const [activeItem, setActiveItem] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();

    const edit = async () => {
      await myRequest("/convform", {
        flow: flow,
        func: "edit",
        item_type: element,
        name: activeItem.name,
        data: activeItem,
      }).then((e) => {
        fetchProof();
        fetchItems();
        e.success
          ? setLastEvent(`edited ${element} ${activeItem.name || ""}`)
          : setLastEvent(`couldn't edit ${element} ${activeItem.name || ""}`);
      });
    };
    edit();
    setChanges(false);
  };

  useEffect(() => {
    setActiveItem(elementData);
  }, [element, elementData]);

  return (
    <div className="form-container">
      <h5>
        {element} {activeItem.name || flow}
      </h5>
      <ul className="edit-bricks-listing">
        {fields.length &&
          fields
            .filter(([f]) => {
              return f != "name";
            })
            .map(([f, fType], i) => {
              console.log("f", f, fType, i);
              return (
                <EditBrick
                  key={i}
                  label={f}
                  type={fType}
                  setChanges={setChanges}
                  setActiveItem={setActiveItem}
                  activeItem={activeItem}
                />
              );
            })}
      </ul>
      <form className="editor-input" onSubmit={handleSubmit}>
        <div className="editor-submit">
          <button className="submit admin-button">📨</button>
        </div>
      </form>
    </div>
  );
};

AbstractForm.propTypes = {
  element: PropTypes.string.isRequired,
  fields: PropTypes.object.isRequired,
  elementData: PropTypes.object.isRequired,
  flow: PropTypes.string.isRequired,
  setLastEvent: PropTypes.func.isRequired,
  fetchProof: PropTypes.func.isRequired,
  fetchItems: PropTypes.func.isRequired,
};

export default AbstractForm;
