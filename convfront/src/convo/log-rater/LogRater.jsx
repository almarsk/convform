import CheckBox from "./Checkbox";
import "./log-rater.scss";

const LogRater = ({ convo, setConvo }) => {
  return (
    <>
      <p className="log-rater-parent">
        Zvolte odpovědi chatbota, které{" "}
        <ul>
          <li>
            vás <b>zaujaly</b>{" "}
          </li>
          <li>
            nebo se vám <b>nelíbily</b>:
          </li>
        </ul>
      </p>
      {convo.map((turn, renderIndex) => {
        return (
          <>
            <div key={renderIndex} className="log-rater-item">
              <div className="checkbox-box">
                {turn.who == "bot" ? (
                  <CheckBox
                    onCheck={() => {
                      setConvo(
                        convo.map((item, onCheckIndex) =>
                          onCheckIndex == renderIndex
                            ? {
                                ...item,
                                checked: !item.checked,
                              }
                            : { ...item },
                        ),
                      );
                    }}
                  />
                ) : (
                  ""
                )}
              </div>
              <span className="log-rater-turn">
                {turn.who == "bot" ? "🤖" : "🗣️"}: {turn.text}
              </span>
            </div>
            <div>
              {turn.checked ? (
                <>
                  <p className="log-rater-question">
                    Co na této odpovědi vás <b>zaujalo</b>?
                  </p>
                  <textarea
                    required
                    className="eval-field input-field content"
                    onChange={(e) => {
                      setConvo(
                        convo.map((check, onCheckIndex) =>
                          onCheckIndex == renderIndex
                            ? {
                                ...check,
                                comment: e.target.value,
                              }
                            : { ...check },
                        ),
                      );
                    }}
                  />
                </>
              ) : (
                ""
              )}
            </div>
          </>
        );
      })}
    </>
  );
};

LogRater.propTypes = {};

export default LogRater;
