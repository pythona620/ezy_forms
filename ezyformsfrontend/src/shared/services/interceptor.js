import axios from "axios";
import { loadValue } from "../../Components/loader/loader";
import { toast } from "vue3-toastify";
// import { tokens } from "../apiurls";
const axiosInstance = axios.create();
axiosInstance.interceptors.request.use(
  (config) => {
    // if (config.url.includes("resource")) {
    //   loadValue.value = false;
    // } else {
    loadValue.value = true;
    // }
    // config.withCredentials = true;
    // config.headers = {
    //     Authorization: `token ${tokens.Apikey}:${tokens.secretkey}`
    // }
    return config;
  },
  (error) => {
    loadValue.value = false;

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
    if (error.response) {
      const statusText = error.response.statusText.toLowerCase();
      if (error.response.status === 400) {
        toast.error(`Bad Request: ${statusText}`, { transition: "zoom" });
      } else if (error.response.status === 401) {
        // Unauthorized: 
        toast.error(`${error.response.data.message}`, { transition: "zoom" });
      } else if (error.response.status === 403) {
        // Forbidden:
        toast.error(` ${error.response.data.exc_type}`, { transition: "zoom" });
      } else if (error.response.status === 404) {
        toast.error(`Not Found: ${statusText}`, { transition: "zoom" });
      } else if (error.response.status === 500) {
        toast.error(`Internal Server Error: ${statusText}`, { transition: "zoom" });
      } else {
        toast.error(`Error ${error.response.status}: ${statusText}`, { transition: "zoom" });
      }
    } else if (error.request) {
      toast.error("No response received: Please check your network connection");
    } else {
      toast.error("Error setting up request: " + error.statusText);
    }

    return Promise.reject(error);
  }
);
export default axiosInstance;
