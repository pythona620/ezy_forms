import axiosInstance from "./interceptor";
import { apis } from "../apiurls";

export default function postResourceData(
  doctype,
  fileds,
  filters,
  itemsPerPage,
  limit_start
) {
  return new Promise((resolve, reject) => {
    const queryParams = {
      limit_page_length: itemsPerPage,
      fields: JSON.stringify(fileds),
      limit_start: limit_start,
      filters: JSON.stringify(filters),
    };

    axiosInstance
      .post(`${apis.resource}${doctype}`, { params: queryParams })
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
