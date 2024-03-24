import PropTypes from "prop-types";

const LoginPage = ({ onLogin, unsuccess }) => {
  const handleSubmit = async (e) => {
    const login_attempt = new FormData(e.target);
    e.preventDefault();
    await onLogin(login_attempt.get("nick"), login_attempt.get("pass"));
  };

  return (
    <>
      <form onSubmit={(e) => handleSubmit(e)}>
        <h3>Login</h3>
        <div>
          <input
            name="nick"
            className="input-field login-field"
            type="text"
            placeholder="Nick"
            autoComplete="username"
            required
          ></input>
        </div>
        <div>
          <input
            name="pass"
            className="input-field login-field"
            type="password"
            placeholder="Pass"
            autoComplete="current-password"
            required
          ></input>
        </div>
        <div>
          <button className="submit" type="submit">
            ↵
          </button>
          <p>{unsuccess ? "Invalid credentials" : ""}</p>
        </div>
      </form>
    </>
  );
};

LoginPage.propTypes = {
  onLogin: PropTypes.func.isRequired,
  unsuccess: PropTypes.bool,
};

export default LoginPage;
