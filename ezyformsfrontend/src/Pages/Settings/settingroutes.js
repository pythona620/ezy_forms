const SettingsPage = () => import("./SettingsPage.vue");
const ProfileComp = () => import("./ProfileComp.vue");
const NotificationComp = () => import("./NotificationComp.vue");
const UserManageent = () => import("./UserManagement.vue");
const WorkFLow = () => import("./WorkFlow.vue");
const Roles = () => import("./RolesComp.vue");
const RolesMatrix = () => import("./RolesMatrix.vue");
const Categories = () => import("./Catagories.vue");
const ActivityLog = () => import("./ActivitLog.vue");

const settingRoutes = [
  {
    path: "/settings",
    component: SettingsPage,
    redirect: "/settings/usermanagement",

    children: [
      {
        path: "usermanagement",
        component: UserManageent,
        name: "UserManageent",
      },
      {
        path: "profile",
        component: ProfileComp,
        name: "ProfileComp",
      },
      {
        path: "notifications",
        component: NotificationComp,
        name: "NotificationComp",
      },
      {
        path: "workflow",
        component: WorkFLow,
        name: "WorkFLow",
      },
      {
        path: "role",
        component: Roles,
        name: "Roles",
      },
      {
        path: "rolematrix",
        component: RolesMatrix,
        name: "RolesMatrix",
      },

      {
        path: "categories",
        component: Categories,
        name: "Categories",
      },
      {
        path: "activitylog",
        component: ActivityLog,
        name: "ActivityLog",
      },
    ],
  },
];
export default settingRoutes;
