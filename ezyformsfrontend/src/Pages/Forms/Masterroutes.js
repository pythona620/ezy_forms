const MasterPage = () => import("./MasterPage.vue");
const AccountsComp = () => import("./AccountsComp.vue");
const AdminComp = () => import("./AdminComp.vue");
// const FormPage = () => import("./FormPage.vue");
const ItComp = () => import("./ItComp.vue");
const HrComp = () => import("./HrComp.vue");
const SalesComp = () => import("./SalesComp.vue");
import FinanaceComp from "./FinanaceComp.vue";
import FrontOffice from "./FrontOffice.vue";
import HouseKeepingComp from "./HouseKeepingComp.vue";
import RevenueComp from "./RevenueComp.vue";
import FBComp from "./F&BComp.vue";
const Masterroutes = [
  {
    path: "/forms",
    component: MasterPage,
    redirect: "/forms/it",

    children: [
      {
        path: "it",
        component: ItComp,

        name: "ItComp",
      },
      {
        path: "revenue",
        component: RevenueComp,

        name: "RevenueComp",
      },
      {
        path: "finance",
        component: FinanaceComp,

        name: "FinanaceComp",
      },
      {
        path: "frontoffice",
        name: "FrontOffice",
        component: FrontOffice,
      },
      {
        path: "housekeeping",
        name: "HouseKeepingComp",
        component: HouseKeepingComp,
      },
      {
        path: "hr",
        name: "HrComp",
        component: HrComp,
      },
      {
        path: "sales",
        name: "SalesComp",
        component: SalesComp,
      },
      {
        path: "accounts",
        name: "AccountsComp",
        component: AccountsComp,
      },
      {
        path: "admin",
        name: "AdminComp",
        component: AdminComp,
      },
      {
        path: "f&b",
        name: "FBComp",
        component: FBComp,
      },
    ],
  },
];
export default Masterroutes;
