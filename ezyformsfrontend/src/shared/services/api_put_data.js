import axiosInstance from "./interceptor";
import { apis } from "../apiurls";
import { toast } from "vue3-toastify";
import { showSuccess } from "./toast";

export default function putResourceData(doctype, data, id) {
  return new Promise((resolve, reject) => {
    axiosInstance
      .put(`${apis.resource}${doctype}/${id}`, data)
      .then((response) => {
        showSuccess("Updated", { autoClose: 500 });
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
