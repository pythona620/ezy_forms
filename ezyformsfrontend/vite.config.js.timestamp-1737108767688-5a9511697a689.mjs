var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};

// ../../../sites/common_site_config.json
var require_common_site_config = __commonJS({
  "../../../sites/common_site_config.json"(exports, module) {
    module.exports = {
      allow_cors: "*",
      background_workers: 1,
      default_site: "test.in",
      developer_mode: 1,
      file_watcher_port: 6787,
      frappe_user: "caratred",
      gunicorn_workers: 9,
      live_reload: true,
      rebase_on_pull: false,
      redis_cache: "redis://127.0.0.1:13000",
      redis_queue: "redis://127.0.0.1:11000",
      redis_socketio: "redis://127.0.0.1:13000",
      restart_supervisor_on_update: false,
      restart_systemd_on_update: false,
      serve_default_site: true,
      shallow_clone: true,
      socketio_port: 9e3,
      use_redis_auth: false,
      webserver_port: 8e3
    };
  }
});

// vite.config.js
import path from "path";
import { defineConfig, loadEnv } from "file:///home/caratred/frappe-bench/apps/ezy_forms/ezyformsfrontend/node_modules/vite/dist/node/index.js";
import vue from "file:///home/caratred/frappe-bench/apps/ezy_forms/ezyformsfrontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";

// proxyOptions.js
var common_site_config = require_common_site_config();
var { webserver_port } = common_site_config;
var proxyOptions_default = {
  "^/(app|api|assets|files|private)": {
    target: `http://127.0.0.1:${webserver_port}`,
    ws: true,
    router: function(req) {
      const site_name = req.headers.host.split(":")[0];
      return `http://${site_name}:${webserver_port}`;
    }
  }
};

// vite.config.js
var __vite_injected_original_dirname = "/home/caratred/frappe-bench/apps/ezy_forms/ezyformsfrontend";
var vite_config_default = defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());
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
      router: function(req) {
        return `${env.VITE_API_BASE_URL}`;
      }
    }
  };
  return {
    plugins: [vue()],
    server: {
      port: 8080,
      proxy: updatedProxyOptions
      // Use updated proxy settings
    },
    resolve: {
      alias: {
        "@": path.resolve(__vite_injected_original_dirname, "src")
      }
    },
    build: {
      // outDir: '../esl/public/frontend',
      outDir: `../${path.basename(path.resolve(".."))}/public/ezyformsfrontend`,
      emptyOutDir: true,
      target: "es2015"
    },
    // Optionally define process.env for use in your app
    define: {
      "process.env": env
    }
  };
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vLi4vLi4vc2l0ZXMvY29tbW9uX3NpdGVfY29uZmlnLmpzb24iLCAidml0ZS5jb25maWcuanMiLCAicHJveHlPcHRpb25zLmpzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJ7XG4gXCJhbGxvd19jb3JzXCI6IFwiKlwiLFxuIFwiYmFja2dyb3VuZF93b3JrZXJzXCI6IDEsXG4gXCJkZWZhdWx0X3NpdGVcIjogXCJ0ZXN0LmluXCIsXG4gXCJkZXZlbG9wZXJfbW9kZVwiOiAxLFxuIFwiZmlsZV93YXRjaGVyX3BvcnRcIjogNjc4NyxcbiBcImZyYXBwZV91c2VyXCI6IFwiY2FyYXRyZWRcIixcbiBcImd1bmljb3JuX3dvcmtlcnNcIjogOSxcbiBcImxpdmVfcmVsb2FkXCI6IHRydWUsXG4gXCJyZWJhc2Vfb25fcHVsbFwiOiBmYWxzZSxcbiBcInJlZGlzX2NhY2hlXCI6IFwicmVkaXM6Ly8xMjcuMC4wLjE6MTMwMDBcIixcbiBcInJlZGlzX3F1ZXVlXCI6IFwicmVkaXM6Ly8xMjcuMC4wLjE6MTEwMDBcIixcbiBcInJlZGlzX3NvY2tldGlvXCI6IFwicmVkaXM6Ly8xMjcuMC4wLjE6MTMwMDBcIixcbiBcInJlc3RhcnRfc3VwZXJ2aXNvcl9vbl91cGRhdGVcIjogZmFsc2UsXG4gXCJyZXN0YXJ0X3N5c3RlbWRfb25fdXBkYXRlXCI6IGZhbHNlLFxuIFwic2VydmVfZGVmYXVsdF9zaXRlXCI6IHRydWUsXG4gXCJzaGFsbG93X2Nsb25lXCI6IHRydWUsXG4gXCJzb2NrZXRpb19wb3J0XCI6IDkwMDAsXG4gXCJ1c2VfcmVkaXNfYXV0aFwiOiBmYWxzZSxcbiBcIndlYnNlcnZlcl9wb3J0XCI6IDgwMDBcbn0iLCAiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIi9ob21lL2NhcmF0cmVkL2ZyYXBwZS1iZW5jaC9hcHBzL2V6eV9mb3Jtcy9lenlmb3Jtc2Zyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvaG9tZS9jYXJhdHJlZC9mcmFwcGUtYmVuY2gvYXBwcy9lenlfZm9ybXMvZXp5Zm9ybXNmcm9udGVuZC92aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vaG9tZS9jYXJhdHJlZC9mcmFwcGUtYmVuY2gvYXBwcy9lenlfZm9ybXMvZXp5Zm9ybXNmcm9udGVuZC92aXRlLmNvbmZpZy5qc1wiO2ltcG9ydCBwYXRoIGZyb20gXCJwYXRoXCI7XG5pbXBvcnQgeyBkZWZpbmVDb25maWcsIGxvYWRFbnYgfSBmcm9tIFwidml0ZVwiO1xuaW1wb3J0IHZ1ZSBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tdnVlXCI7XG5cbi8vIFVwZGF0ZSB0aGlzIGltcG9ydCBiYXNlZCBvbiBob3cgeW91IGV4cG9ydCBwcm94eSBvcHRpb25zXG5pbXBvcnQgcHJveHlPcHRpb25zIGZyb20gXCIuL3Byb3h5T3B0aW9uc1wiO1xuXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoKHsgbW9kZSB9KSA9PiB7XG5cdC8vIExvYWQgZW52aXJvbm1lbnQgdmFyaWFibGVzIGJhc2VkIG9uIHRoZSBjdXJyZW50IG1vZGVcblx0Y29uc3QgZW52ID0gbG9hZEVudihtb2RlLCBwcm9jZXNzLmN3ZCgpKTtcblxuXHQvLyBVcGRhdGUgcHJveHlPcHRpb25zIHRvIHVzZSBlbnYgdmFyaWFibGVzIGlmIG5lZWRlZFxuXHRjb25zdCB1cGRhdGVkUHJveHlPcHRpb25zID0ge1xuXHRcdC8vICdeLyhhcHB8YXBpfGFzc2V0c3xmaWxlc3xwcml2YXRlKSc6IHtcblx0XHQvLyAgdGFyZ2V0OiBlbnYuVklURV9BUElfQkFTRV9VUkwsIC8vIEZhbGxiYWNrIGlmIG5vdCBkZWZpbmVkXG5cdFx0Ly8gIHdzOiB0cnVlLFxuXHRcdC8vICByb3V0ZXI6IGZ1bmN0aW9uIChyZXEpIHtcblx0XHQvLyAgICAgIGNvbnN0IHNpdGVfbmFtZSA9IHJlcS5oZWFkZXJzLmhvc3Quc3BsaXQoJzonKVswXTtcblx0XHQvLyAgICAgIHJldHVybiBgJHtlbnYuVklURV9BUElfQkFTRV9VUkx9YDsgLy8gVXNlIGVudmlyb25tZW50IHZhcmlhYmxlXG5cdFx0Ly8gIH1cblx0XHQvLyB9XG5cdFx0XCJeLyhhcHB8YXBpfGFzc2V0c3xmaWxlc3xwcml2YXRlKVwiOiB7XG5cdFx0XHR0YXJnZXQ6IGVudi5WSVRFX0FQSV9CQVNFX1VSTCxcblx0XHRcdHdzOiB0cnVlLFxuXHRcdFx0cm91dGVyOiBmdW5jdGlvbiAocmVxKSB7XG5cdFx0XHRcdHJldHVybiBgJHtlbnYuVklURV9BUElfQkFTRV9VUkx9YDsgLy8gVGhpcyB3aWxsIHJvdXRlIHRvIHRoZSBjb3JyZWN0IGJhY2tlbmRcblx0XHRcdH0sXG5cdFx0fSxcblx0fTtcblxuXHRyZXR1cm4ge1xuXHRcdHBsdWdpbnM6IFt2dWUoKV0sXG5cdFx0c2VydmVyOiB7XG5cdFx0XHRwb3J0OiA4MDgwLFxuXHRcdFx0cHJveHk6IHVwZGF0ZWRQcm94eU9wdGlvbnMsIC8vIFVzZSB1cGRhdGVkIHByb3h5IHNldHRpbmdzXG5cdFx0fSxcblx0XHRyZXNvbHZlOiB7XG5cdFx0XHRhbGlhczoge1xuXHRcdFx0XHRcIkBcIjogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgXCJzcmNcIiksXG5cdFx0XHR9LFxuXHRcdH0sXG5cdFx0YnVpbGQ6IHtcblx0XHRcdC8vIG91dERpcjogJy4uL2VzbC9wdWJsaWMvZnJvbnRlbmQnLFxuXHRcdFx0b3V0RGlyOiBgLi4vJHtwYXRoLmJhc2VuYW1lKHBhdGgucmVzb2x2ZShcIi4uXCIpKX0vcHVibGljL2V6eWZvcm1zZnJvbnRlbmRgLFxuXHRcdFx0ZW1wdHlPdXREaXI6IHRydWUsXG5cdFx0XHR0YXJnZXQ6IFwiZXMyMDE1XCIsXG5cdFx0fSxcblx0XHQvLyBPcHRpb25hbGx5IGRlZmluZSBwcm9jZXNzLmVudiBmb3IgdXNlIGluIHlvdXIgYXBwXG5cdFx0ZGVmaW5lOiB7XG5cdFx0XHRcInByb2Nlc3MuZW52XCI6IGVudixcblx0XHR9LFxuXHR9O1xufSk7XG4iLCAiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIi9ob21lL2NhcmF0cmVkL2ZyYXBwZS1iZW5jaC9hcHBzL2V6eV9mb3Jtcy9lenlmb3Jtc2Zyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvaG9tZS9jYXJhdHJlZC9mcmFwcGUtYmVuY2gvYXBwcy9lenlfZm9ybXMvZXp5Zm9ybXNmcm9udGVuZC9wcm94eU9wdGlvbnMuanNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL2hvbWUvY2FyYXRyZWQvZnJhcHBlLWJlbmNoL2FwcHMvZXp5X2Zvcm1zL2V6eWZvcm1zZnJvbnRlbmQvcHJveHlPcHRpb25zLmpzXCI7Y29uc3QgY29tbW9uX3NpdGVfY29uZmlnID0gcmVxdWlyZSgnLi4vLi4vLi4vc2l0ZXMvY29tbW9uX3NpdGVfY29uZmlnLmpzb24nKTtcbmNvbnN0IHsgd2Vic2VydmVyX3BvcnQgfSA9IGNvbW1vbl9zaXRlX2NvbmZpZztcblxuZXhwb3J0IGRlZmF1bHQge1xuXHQnXi8oYXBwfGFwaXxhc3NldHN8ZmlsZXN8cHJpdmF0ZSknOiB7XG5cdFx0dGFyZ2V0OiBgaHR0cDovLzEyNy4wLjAuMToke3dlYnNlcnZlcl9wb3J0fWAsXG5cdFx0d3M6IHRydWUsXG5cdFx0cm91dGVyOiBmdW5jdGlvbihyZXEpIHtcblx0XHRcdGNvbnN0IHNpdGVfbmFtZSA9IHJlcS5oZWFkZXJzLmhvc3Quc3BsaXQoJzonKVswXTtcblx0XHRcdHJldHVybiBgaHR0cDovLyR7c2l0ZV9uYW1lfToke3dlYnNlcnZlcl9wb3J0fWA7XG5cdFx0fVxuXHR9XG59O1xuIl0sCiAgIm1hcHBpbmdzIjogIjs7Ozs7O0FBQUE7QUFBQTtBQUFBO0FBQUEsTUFDQyxZQUFjO0FBQUEsTUFDZCxvQkFBc0I7QUFBQSxNQUN0QixjQUFnQjtBQUFBLE1BQ2hCLGdCQUFrQjtBQUFBLE1BQ2xCLG1CQUFxQjtBQUFBLE1BQ3JCLGFBQWU7QUFBQSxNQUNmLGtCQUFvQjtBQUFBLE1BQ3BCLGFBQWU7QUFBQSxNQUNmLGdCQUFrQjtBQUFBLE1BQ2xCLGFBQWU7QUFBQSxNQUNmLGFBQWU7QUFBQSxNQUNmLGdCQUFrQjtBQUFBLE1BQ2xCLDhCQUFnQztBQUFBLE1BQ2hDLDJCQUE2QjtBQUFBLE1BQzdCLG9CQUFzQjtBQUFBLE1BQ3RCLGVBQWlCO0FBQUEsTUFDakIsZUFBaUI7QUFBQSxNQUNqQixnQkFBa0I7QUFBQSxNQUNsQixnQkFBa0I7QUFBQSxJQUNuQjtBQUFBO0FBQUE7OztBQ3BCbVcsT0FBTyxVQUFVO0FBQ3BYLFNBQVMsY0FBYyxlQUFlO0FBQ3RDLE9BQU8sU0FBUzs7O0FDRnFWLElBQU0scUJBQXFCO0FBQ2hZLElBQU0sRUFBRSxlQUFlLElBQUk7QUFFM0IsSUFBTyx1QkFBUTtBQUFBLEVBQ2Qsb0NBQW9DO0FBQUEsSUFDbkMsUUFBUSxvQkFBb0IsY0FBYztBQUFBLElBQzFDLElBQUk7QUFBQSxJQUNKLFFBQVEsU0FBUyxLQUFLO0FBQ3JCLFlBQU0sWUFBWSxJQUFJLFFBQVEsS0FBSyxNQUFNLEdBQUcsRUFBRSxDQUFDO0FBQy9DLGFBQU8sVUFBVSxTQUFTLElBQUksY0FBYztBQUFBLElBQzdDO0FBQUEsRUFDRDtBQUNEOzs7QURaQSxJQUFNLG1DQUFtQztBQU96QyxJQUFPLHNCQUFRLGFBQWEsQ0FBQyxFQUFFLEtBQUssTUFBTTtBQUV6QyxRQUFNLE1BQU0sUUFBUSxNQUFNLFFBQVEsSUFBSSxDQUFDO0FBR3ZDLFFBQU0sc0JBQXNCO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBLElBUzNCLG9DQUFvQztBQUFBLE1BQ25DLFFBQVEsSUFBSTtBQUFBLE1BQ1osSUFBSTtBQUFBLE1BQ0osUUFBUSxTQUFVLEtBQUs7QUFDdEIsZUFBTyxHQUFHLElBQUksaUJBQWlCO0FBQUEsTUFDaEM7QUFBQSxJQUNEO0FBQUEsRUFDRDtBQUVBLFNBQU87QUFBQSxJQUNOLFNBQVMsQ0FBQyxJQUFJLENBQUM7QUFBQSxJQUNmLFFBQVE7QUFBQSxNQUNQLE1BQU07QUFBQSxNQUNOLE9BQU87QUFBQTtBQUFBLElBQ1I7QUFBQSxJQUNBLFNBQVM7QUFBQSxNQUNSLE9BQU87QUFBQSxRQUNOLEtBQUssS0FBSyxRQUFRLGtDQUFXLEtBQUs7QUFBQSxNQUNuQztBQUFBLElBQ0Q7QUFBQSxJQUNBLE9BQU87QUFBQTtBQUFBLE1BRU4sUUFBUSxNQUFNLEtBQUssU0FBUyxLQUFLLFFBQVEsSUFBSSxDQUFDLENBQUM7QUFBQSxNQUMvQyxhQUFhO0FBQUEsTUFDYixRQUFRO0FBQUEsSUFDVDtBQUFBO0FBQUEsSUFFQSxRQUFRO0FBQUEsTUFDUCxlQUFlO0FBQUEsSUFDaEI7QUFBQSxFQUNEO0FBQ0QsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
