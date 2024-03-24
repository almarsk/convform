import myRequest from "../myRequest";
import basename from "../basename.jsx";

const Start = () => {
  return (
    <>
      <p id="intro-text">
        Můžeme začít. Pokud bude robot říkat nesmysly, ukončete ho červeným
        tlačítkem
      </p>
      <form
        className="content-box"
        onSubmit={async (e) => {
          e.preventDefault();
          await myRequest("/start", {}).then(() => {
            window.location.href = basename + "/";
          });
        }}
      >
        <div className="content-box input">
          <button className="submit">↵</button>
        </div>
      </form>
    </>
  );
};

export default Start;
