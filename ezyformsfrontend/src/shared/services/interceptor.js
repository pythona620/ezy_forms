import axios from "axios";
import { loadValue } from "../../Components/loader/loader";
import { showError } from "./toast";
const axiosInstance = axios.create();
axiosInstance.interceptors.request.use(
  (config) => {
    loadValue.value = true;
    return config;
  },
  (error) => {
    loadValue.value = false;
    showError("Request error: " + (error.message || "Unknown error"));
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    loadValue.value = false;

    return response.data;
  },
  (error) => {
    loadValue.value = false;

    const status = error?.response?.status;
    const statusText = error?.response?.statusText || "Error";

    // Helper to parse and show server messages safely
    const showServerMessages = (data) => {
      try {
        const messages = JSON.parse(data._server_messages || "[]");
        if (Array.isArray(messages)) {
          messages.forEach((msg) => {
            const parsed = JSON.parse(msg);
            let message = parsed.message?.replace(/\s*\(.*?\)\s*/g, "").trim();
            showError(message || "Server error", { transition: "zoom" });
          });
        }
      } catch (e) {
        showError("Failed to parse server messages", { transition: "zoom" });
      }
    };

    if (error.response) {
      switch (status) {
        case 400:
          showError("Bad Request", { transition: "zoom" });
          break;
        case 401:
          showError(error.response.data?.message || "Unauthorized", { transition: "zoom" });
          break;
        case 403:
          showError("Access forbidden. You don't have permission to perform this action.", { transition: "zoom" });
          break;
        case 404:
        case 417:
          showServerMessages(error.response.data);
          break;
        case 409:
          showError("Conflict: The data already exists.");
          break;
        case 500:
          // Don't expose technical error details to users
          showError("An internal error occurred. Please try again later.", { transition: "zoom" });
          // Log the actual error for debugging
          console.error('Server Error:', error.response.data);
          break;
        default:
          showError(`${status}: ${statusText}`, { transition: "zoom" });
          break;
      }
    } else if (error.request) {
      showError("No response received: Please check your network connection", { transition: "zoom" });
    } else {
      showError((error.message || "Unknown error"), { transition: "zoom" });
    }

    return Promise.reject(error);
  }
);
export default axiosInstance;
