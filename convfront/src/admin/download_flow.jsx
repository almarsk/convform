import myRequest from "../myRequest";

const download_flow = async (bot) => {
  try {
    const response = await myRequest("/export_flow", { name: bot });

    // Check if the response contains the 'flow' object
    if (response.flow) {
      const blob = new Blob([JSON.stringify(response.flow)], {
        type: "application/json",
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${bot}.json`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      console.error("The 'flow' object is missing from the response data.");
    }
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
  }
};

export default download_flow;
