import path from "path";
import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// Update this import based on how you export proxy options
import proxyOptions from "./proxyOptions";

export default defineConfig(({ mode }) => {
  // Load environment variables based on the current mode
  const env = loadEnv(mode, process.cwd());

  // Update proxyOptions to use env variables if needed
  const updatedProxyOptions = {
    // '^/(app|api|assets|files|private)': {
    //  target: env.VITE_API_BASE_URL, // Fallback if not defined
    //  ws: true,
    //  router: function (req) {
    //      const site_name = req.headers.host.split(':')[0];
    //      return `${env.VITE_API_BASE_URL}`; // Use environment variable
    //  }
    // }
    "^/(app|api|assets|files|private)": {
      target: env.VITE_API_BASE_URL,
      ws: true,
      router: function (req) {
        return `${env.VITE_API_BASE_URL}`; // This will route to the correct backend
      },
    },
  };

  return {
    plugins: [vue()],
    server: {
      port: 8080,
      proxy: updatedProxyOptions, // Use updated proxy settings
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
    build: {
      // outDir: '../esl/public/frontend',
      outDir: `../${path.basename(path.resolve(".."))}/public/frontend`,
      emptyOutDir: true,
      target: "es2015",
    },
    // Optionally define process.env for use in your app
    define: {
      "process.env": env,
    },
  };
});
