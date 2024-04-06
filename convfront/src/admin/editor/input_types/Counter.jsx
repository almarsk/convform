import PropTypes from "prop-types";
import { useState } from "react";
import slugify from "slugify";

const Counter = ({ label, activeItem, setActiveItem }) => {
  const [newValue, setNewValue] = useState("");
  return (
    <div className="counter">
      {typeof activeItem[label] == "object" &&
        Object.entries(activeItem[label]).map(([state, usage], i) => {
          return (
            <div className="counter-item" key={i}>
              <p>{state}</p>
              <div>
                <input
                  min={0}
                  type="number"
                  className={`input-field narrow`}
                  name={label}
                  placeholder={label}
                  value={usage}
                  onChange={(e) => {
                    setActiveItem((prevActive) => {
                      return {
                        ...prevActive,
                        [label]: {
                          ...activeItem[label],
                          [state]: parseInt(e.target.value),
                        },
                      };
                    });
                  }}
                />
              </div>
            </div>
          );
        })}

      <input
        className="list-input single-line"
        onChange={(e) => setNewValue(e.target.value)}
        value={newValue}
        placeholder="new state usage"
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            if (
              newValue &&
              !Object.prototype.hasOwnProperty.call(activeItem[label], newValue)
            ) {
              setActiveItem((prev) => ({
                ...prev,
                [label]: { ...prev[label], [slugify(newValue)]: 0 },
              }));
            }
            setNewValue("");
          }
        }}
      />
    </div>
  );
};

Counter.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default Counter;
