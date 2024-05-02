import { useEffect, useState } from "react";

import PropTypes from "prop-types";
import EditBrick from "./EditBrick";

const AbstractForm = ({
  element,
  elementData,
  fields,
  flow,
  setActivePanel,
  handleSubmit,
  onChange,
  disableSubmit,
}) => {
  const [, setChanges] = useState(false);
  const [activeItem, setActiveItem] = useState({});

  useEffect(() => {
    // going back to listing if elementData doesn't arrive
    if (!elementData && setActivePanel) setActivePanel(`list-${element}s`);
    setActiveItem(elementData);
  }, [element, elementData]);

  useEffect(() => {
    onChange && onChange(activeItem);
  }, [activeItem]);

  return (
    <div className="form-container">
      <h5>
        {element} {activeItem ? activeItem.name || flow : ""}
      </h5>
      <ul className="edit-bricks-listing">
        {fields.length &&
          fields
            .filter(([f]) => {
              return f != "name";
            })
            .map(([f, fType], i) => {
              return (
                <EditBrick
                  element={element}
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
      {!disableSubmit && (
        <form
          className="editor-input"
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit({ element, activeItem, setChanges });
          }}
        >
          <div className="editor-submit">
            <button className="submit admin-button">📨</button>
          </div>
        </form>
      )}
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
