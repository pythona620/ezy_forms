import axiosInstance from "./interceptor";
import { apis } from "../apiurls";
import { toast } from "vue3-toastify";

export default function putResourceData(doctype, data, id) {
  return new Promise((resolve, reject) => {
    axiosInstance
      .put(`${apis.resource}${doctype}/${id}`, data)
      .then((response) => {
        toast.success("Updated", { autoClose: 500 });
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
