export const domain = process.env.NODE_ENV === "production" ? "" : "/api"; //=  "/api";   process.env.NODE_ENV === 'production' ? '/' : '/api'
export const fileDomain = "";

export const doctypes = {
  poschecks: "POS Checks",
};

export const apis = {
  resource: domain + `/api/resource/`,
  uploadfile: domain + `/api/method/upload_file`,
};
// export const tokens = {
//   Apikey: "1812146a6f090f1",
//   secretkey: "7a5e80cad93659f",

// }
