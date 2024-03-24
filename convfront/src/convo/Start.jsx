import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import myRequest from "../myRequest";

const Start = () => {
  const navigate = useNavigate(); // Access navigate function from the hook

  useEffect(() => {
    // Optional: You can include any initialization logic here if needed
  }, []);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    await myRequest("/start", {});
    navigate("/"); // Navigate to "/" after the form is submitted
  };

  return (
    <>
      <p id="intro-text">
        Můžeme začít. Pokud bude robot říkat nesmysly, ukončete ho červeným
        tlačítkem
      </p>
      <form className="content-box" onSubmit={handleFormSubmit}>
        <div className="content-box input">
          <button type="submit" className="submit">
            ↵
          </button>
        </div>
      </form>
    </>
  );
};

export default Start;
