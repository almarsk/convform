import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import Draggable from "react-draggable";
import myRequest from "../myRequest";
import { useContext } from "react";
import { IssuesContext } from "../IssuesContext";

const DraggableLabel = ({ bot, statusSuccess, setBotsList }) => {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [originalPosition, setOriginalPosition] = useState({ x: 0, y: 0 });
  const [dropPosition, setDropPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [hit, setHit] = useState(false);

  const { setIssues } = useContext(IssuesContext);

  const handleDrag = (e, ui) => {
    const { x, y } = position;
    setPosition({ x: x + ui.deltaX, y: y + ui.deltaY });
  };

  const handleStop = (e) => {
    const rect = e.target.getBoundingClientRect();
    const absoluteX = rect.left + window.pageXOffset;
    const absoluteY = rect.top + window.pageYOffset;
    setHit(true);
    setIsDragging(false);
    setPosition(originalPosition);
    setDropPosition({ x: absoluteX, y: absoluteY });
  };

  const onStart = () => {
    const { x, y } = position;
    setOriginalPosition({ x, y });
    setIsDragging(true);
  };

  const findElementUnderTopmost = (element, selector) => {
    while (element) {
      if (element.classList.contains(selector)) {
        return element;
      }
      element = element.parentElement;
    }
    return null;
  };

  useEffect(() => {
    if (dropPosition.x == 0 && dropPosition.y == 0) {
      return;
    }

    let droppedOnDiv = document.elementFromPoint(
      dropPosition.x,
      dropPosition.y,
    );
    droppedOnDiv = findElementUnderTopmost(droppedOnDiv, "project-brick");

    if (
      droppedOnDiv &&
      droppedOnDiv.classList.contains("project-brick") &&
      !droppedOnDiv.classList.contains("new-project-form") &&
      !droppedOnDiv.classList.contains("all-flows")
    ) {
      const directoryId = droppedOnDiv.getAttribute("project-id");

      myRequest("/move", {
        item_type: "flow",
        name: bot,
        destination: directoryId,
      }).then(() => {
        setBotsList();
        setHit(false);
      });
    } else {
      setHit(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dropPosition]);

  return (
    <Draggable
      position={position}
      onStop={handleStop}
      onDrag={handleDrag}
      onStart={onStart}
    >
      <div
        onMouseEnter={() => setIssues(`drag to change project`)}
        onMouseLeave={() => setIssues("")}
        className={`flow-label ${isDragging ? "" : "_is-dragging"}`}
        style={{
          color: statusSuccess ? "black" : "grey",
          overflow: isDragging ? "visible" : "auto",
          opacity: hit ? 0 : 100,
        }}
      >
        <b>{bot}</b>
      </div>
    </Draggable>
  );
};

DraggableLabel.propTypes = {
  bot: PropTypes.string.isRequired,
  statusSuccess: PropTypes.bool.isRequired,
  setBotsList: PropTypes.func.isRequired,
};

export default DraggableLabel;
