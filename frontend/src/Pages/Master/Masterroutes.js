const MasterPage = () => import("./MasterPage.vue");
const ActivityPage = () => import("./ActivityLog.vue");
const ArchivePage = () => import("./ArchivePage.vue");
const FormPage = () => import("./FormPage.vue");
const EsignPage = () => import("./EsignPage.vue");
const UsersPage = () => import("./UserPage.vue");
const TrashPage = () => import("./TrashPage.vue");
const Masterroutes = [
  {
    path: "/master",
    component: MasterPage,
    redirect: "/master/Forms",

    children: [
      {
        path: "Forms",
        component: FormPage,

        name: "FormPage",
      },
      {
        path: "Users",
        component: UsersPage,

        name: "UsersPage",
      },
      {
        path: "Activity-Log",
        component: ActivityPage,

        name: "ActivityPage",
      },
      {
        path: "E-Signature",
        name: "EsignPage",
        component: EsignPage,
      },
      {
        path: "Archive",
        name: "ArchivePage",
        component: ArchivePage,
      },
      {
        path: "Trash",
        name: "TrashPage",
        component: TrashPage,
      },
    ],
  },
];
export default Masterroutes;
