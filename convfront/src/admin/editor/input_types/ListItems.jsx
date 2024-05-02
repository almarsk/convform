import PropTypes from "prop-types";

const maxThreeChars = (str) => {
  if (str.length < 3) return str;
  return String(str).split("").slice(0, 3).join("");
};

const ListItems = ({ tags, editTags, vertical, meta }) => {
  return (
    <ul
      className="editor-items-list"
      style={{
        flexDirection: vertical ? "column" : "row",
      }}
    >
      {tags
        ? tags.map((t, i) => (
            <div
              className="editor-tag"
              onClick={() => {
                const newTags = [...tags];
                newTags.splice(i, 1);
                editTags(newTags);
              }}
              key={i}
            >
              {`${meta == "say" ? `${t.prompt ? `prompt - ${maxThreeChars(t.prompt)}` : "say"} - ${t.text}` : t}`}
            </div>
          ))
        : ""}
    </ul>
  );
};

// PropType validations
ListItems.propTypes = {
  tags: PropTypes.array.isRequired,
  editTags: PropTypes.func.isRequired,
  vertical: PropTypes.bool,
  meta: PropTypes.bool,
};

export default ListItems;
