import UserInput from "../app/UserInput";
import BotOutput from "./BotOutput";
import myRequest from "../myRequest";
import { useState, useEffect } from "react";
import "./loader.css";
import { useNavigate } from "react-router-dom";

const Chat = () => {
  const [[loading, minLoading], setLoading] = useState([true, true]);
  const [cStatus, setCStatus] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const navigate = useNavigate(); // Access navigate function from the hook

  useEffect(() => {
    setStartTime(Date.now()); // Record the start time when component mounts
  }, []);

  useEffect(() => {
    if (cStatus == null) {
      const fetchCStatus = async () => await handleCStatus("");
      fetchCStatus();
    }
    if (!minLoading) setLoading([false, minLoading]);

    if (cStatus && cStatus.end) {
      navigate("/"); // Navigate to "/" when cStatus.end is truthy
    }

    if (!loading) console.log(cStatus);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cStatus, loading, navigate]);

  const handleSubmit = async (e) => {
    setLoading([true, true]);
    await handleCStatus(new FormData(e.target).get("content"));
  };

  const handleCStatus = async (userSpeech) => {
    const newCStatus = await myRequest("/bot", [
      userSpeech,
      cStatus,
      Date.now() - startTime,
    ]);
    setCStatus(newCStatus);
    setTimeout(() => setLoading([false, false]), 1500);
  };

  return (
    <>
      <BotOutput
        botSpeech={cStatus && !loading ? cStatus.say : ""}
        loading={loading}
      />
      <UserInput submit={handleSubmit} loading={loading} />
      <button
        onClick={async () => {
          await myRequest("/abort", {});
          navigate("/"); // Navigate to "/" when the button is clicked
        }}
        className="submit"
      >
        🚫
      </button>
    </>
  );
};

export default Chat;
