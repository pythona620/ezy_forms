export const domain = "/api";
//=  "/api";   process.env.NODE_ENV === 'production' ? '/' : '/api'
console.log(domain, "ddddddddddddddddddd");
export const fileDomain = "";

export const doctypes = {
  poschecks: "POS Checks",
  users: "User",
};

export const apis = {
  resource: domain + `/resource/`,
  uploadfile: domain + `/method/upload_file`,
};
// export const tokens = {
//   Apikey: "1812146a6f090f1",
//   secretkey: "7a5e80cad93659f",

// }
