import PropTypes from "prop-types";

import { useState } from "react";
import ListItems from "./ListItems";
import NewItem from "./NewItem";
import { useEffect } from "react";
import myRequest from "../../../myRequest";

const maxThreeChars = (str) => {
  if (str.length < 3) return str;
  return String(str).split("").slice(0, 3).join("");
};

const Say = ({ label, activeItem, setChanges, setActiveItem, element }) => {
  const [isPrompt, setIsPrompt] = useState(false);

  // todo
  const [chains, setChains] = useState([]);
  const [pickedChain, setPickedChain] = useState(0);

  useEffect(() => {
    (() => {
      myRequest("/chains", [element]).then((e) => {
        setChains(e);
      });
    })();
  }, []);

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
                console.log(chains[pickedChain]);
                return {
                  ...prev,
                  [label]: [
                    ...prev[label],
                    // todo
                    { text: newValue, prompt: chains[pickedChain] },
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
