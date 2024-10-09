import axiosInstance from "./interceptor";
import { apis } from "../apiurls";

export default function getResourceData(
  doctype,
  fileds,
  filters,
  itemsPerPage,
  limit_start,
  order_by
) {
  return new Promise((resolve, reject) => {
    const queryParams = {
      fields: JSON.stringify(fileds),
      limit_start: limit_start,
      limit_page_length: itemsPerPage,
      order_by,
      // order_by: `"tab${doctype}. creation desc"`,
    };
    if (filters && filters.length > 0) {
      queryParams.filters = JSON.stringify(filters);
    }
    axiosInstance
      .get(`${apis.resource}${doctype}`, { params: queryParams })
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
