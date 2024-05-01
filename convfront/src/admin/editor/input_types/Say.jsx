import PropTypes from "prop-types";

import { useState } from "react";
import ListItems from "./ListItems";
import NewItem from "./NewItem";
import { useEffect } from "react";

const Say = ({ label, activeItem, setChanges, setActiveItem }) => {
  const [isPrompt, setIsPrompt] = useState(false);

  //todo
  const [chains] = useState([]);
  const [pickedChain, setPickedChain] = useState(0);

  useEffect(() => {
    (() => {
      console.log("todo get chains");
    })();
  });

  const maxThreeChars = (str) => {
    console.log(str);
    if (str.length < 3) return str;
    return String(str).split("").slice(0, 3).join("");
  };

  return (
    <>
      <div className="say-container">
        <div className="input-field say-input">
          <div>
            <button
              className="prompt-button"
              onClick={() => setIsPrompt((prev) => !prev)}
            >
              {isPrompt ? "prompt" : "say"}
            </button>
            {isPrompt && (
              <ul>
                {chains.map((item, index) => {
                  return (
                    <li key={crypto.randomUUID()}>
                      <input
                        type="radio"
                        onChange={() => setPickedChain(index)}
                        checked={index == pickedChain}
                      />
                      <span>{maxThreeChars(item)}</span>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>

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
