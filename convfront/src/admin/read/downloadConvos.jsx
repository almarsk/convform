const formatConvos = (convos) => {
  return JSON.stringify(convos);
};

const downloadConvos = (convos, flow) => {
  const blob = new Blob([formatConvos(convos)], {
    type: "application/json",
  });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `${flow}_export.txt`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export default downloadConvos;
