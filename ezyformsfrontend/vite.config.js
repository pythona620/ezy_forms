// //"IN THE DEVELOPING MODE NEED TO UNCOMMENT THE BELOW CODE"

// import path from 'path';
// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import proxyOptions from './proxyOptions';

// // //  https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue()],
//   server: {
//     port: 8080,
//     proxy: proxyOptions
//   },
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, 'src')
//     }
//   },
//   build: {
//     outDir: '../ezy_forms/public/ezyformsfrontend',
//     emptyOutDir: true,
//     target: 'es2015',
//   },
// });


// //"IN THE PODUCTION MODE NEED TO UNCOMMENT THE BELOW CODE"  

import path from "path";
import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";


// // Update this import based on how you export proxy options
// // import proxyOptions from "./proxyOptions";

export default defineConfig(({ mode }) => {
  //  // Load environment variables based on the current mode
  const env = loadEnv(mode, process.cwd());

  //  // Update proxyOptions to use env variables if needed
  const updatedProxyOptions = {
    "^/(app|api|assets|files|private)": {
      target: env.VITE_API_BASE_URL,
      ws: true,
      router: function (req) {
        return `${env.VITE_API_BASE_URL}`; // // This will route to the correct backend
      },
    },
  };

  return {
    plugins: [vue()],
    server: {
      port: 8080,
      proxy: updatedProxyOptions, // // Use updated proxy settings
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },
    build: {
      // // outDir: '../esl/public/frontend',
      outDir: `../${path.basename(path.resolve(".."))}/public/ezyformsfrontend`,
      emptyOutDir: true,
      target: "es2015",
    },
    // // Optionally define process.env for use in your app
    define: {
      "process.env": env,
    },
  };
});
