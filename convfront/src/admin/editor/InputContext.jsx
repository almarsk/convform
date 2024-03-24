import { createContext, useState } from "react";
import PropTypes from "prop-types";

const InputContext = createContext();

const InputContextProvider = ({ children }) => {
  const [inputUtils, setInputUtils] = useState({});

  return (
    <InputContext.Provider value={{ inputUtils, setInputUtils }}>
      {children}
    </InputContext.Provider>
  );
};

InputContextProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export { InputContext, InputContextProvider };
