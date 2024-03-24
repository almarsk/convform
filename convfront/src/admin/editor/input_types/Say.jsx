import PropTypes from "prop-types";

import { useState } from "react";
import ListItems from "./ListItems";
import NewItem from "./NewItem";

const Say = ({ label, activeItem, setChanges, setActiveItem }) => {
  const [isPrompt, setIsPrompt] = useState(false);

  return (
    <>
      <div className="say-container">
        <div className="input-field say-input">
          <button
            className="prompt-button"
            onClick={() => setIsPrompt((prev) => !prev)}
          >
            {isPrompt ? "prompt" : "say"}
          </button>

          <NewItem
            label={isPrompt ? "prompt" : label}
            area={true}
            addTag={(newValue) => {
              setChanges(true);
              setActiveItem((prev) => {
                return {
                  ...prev,
                  [label]: [
                    ...prev[label],
                    { text: newValue, prompt: isPrompt },
                  ],
                };
              });
            }}
          />
        </div>

        <ListItems
          meta={"say"}
          vertical={true}
          editTags={(newValue) => {
            setChanges(true);
            setActiveItem((prev) => {
              return { ...prev, [label]: newValue };
            });
          }}
          tags={
            activeItem && Object.entries(activeItem).length && activeItem[label]
              ? activeItem[label]
              : []
          }
        />
      </div>
    </>
  );
};

Say.propTypes = {
  label: PropTypes.string.isRequired,
  activeItem: PropTypes.object.isRequired,
  setChanges: PropTypes.func.isRequired,
  setActiveItem: PropTypes.func.isRequired,
};

export default Say;
