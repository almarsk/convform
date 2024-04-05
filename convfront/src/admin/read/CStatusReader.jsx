const CStatusReader = ({ turn, cStatusStructure }) => {
  return (
    <div className="turns-reader">
      {turn &&
        cStatusStructure &&
        cStatusStructure.map(([key], index) => {
          const value = turn.cstatus[key];
          return (
            <pre className="cstatus-item" key={index}>
              {index !== 0 && <hr className="end" />}
              {key + ": "} {JSON.stringify(value, null, 2)}
            </pre>
          );
        })}
    </div>
  );
};

export default CStatusReader;
