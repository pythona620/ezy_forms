// proxyOptions.js
const common_site_config = require("../../../sites/common_site_config.json");
const { webserver_port } = common_site_config;

export default {
  "^/(app|api|assets|files|private)": {
    target: `http://127.0.0.1:${webserver_port}`, // Ensure the API is reachable on this address
    ws: true,
    router: function (req) {
      const site_name = req.headers.host.split(":")[0];
      const targetUrl = `http://${site_name}:${webserver_port}`;
      console.log("Proxying request to:", targetUrl);
      return targetUrl;
    },
  },
};
