import Designations from "./Designations.vue";


const SettingsPage = () => import("./SettingsPage.vue");
const ProfileComp = () => import("./ProfileComp.vue");
const NotificationComp = () => import("./NotificationComp.vue");
const EmployeeComp = () => import("./EmployeeComp.vue");
const WorkFLow = () => import("./WorkFlow.vue");
const Roles = () => import("./RolesComp.vue");
const RolesMatrix = () => import("./RolesMatrix.vue");
const Categories = () => import("./Catagories.vue");
const DepartmentComp = () => import("./DepartmentComp.vue");
const EsignComp = () => import("./EsignComp.vue");
const AuthenticationPage=()=>import("./AuthenticationPage.vue");
const WebEmployee=()=>import("./WebEmployee.vue");
const InactiveEmployee=()=>import("./InactiveEmployee.vue")
const ActivityLog=()=>import("./ActivityLog.vue")
const CreateForm=()=>import("./CreateForm.vue")
const AuditLog=()=>import("./AuditLog.vue");
const AcknowledgementComp=()=>import("./AcknowledgementComp.vue");
const PreDefineForms=()=>import("./PreDefineForms.vue")

const settingRoutes = [
  {
    path: "/settings",
    component: SettingsPage,
    redirect: "/settings/profile",

    children: [
      {
        path: "employee",
        component: EmployeeComp,
        name: "EmployeeComp",
      },
      {
        path: "inactiveEmployee",
        component: InactiveEmployee,
        name: "InactiveEmployee",
      },
      {
        path: "employeeapproval",
        component: WebEmployee,
        name: "WebEmployee",
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
        path: "designations",
        component: Designations,
        name: "Designations"
      },
      {
        path: "department",
        component: DepartmentComp,
        name: "DepartmentComp",
      },
      {
        path: "esign",
        component: EsignComp,
        name: "EsignComp",
      },
      {
        path: "authenticationpage",
        component: AuthenticationPage,
        name: "authenticationpage",
      },
      {
        path: "activitylog",
        component: ActivityLog,
        name: "ActivityLog",
      },
      {
        path: "CreateForm",
        component: CreateForm,
        name: "CreateForm",
      },
      {
        path: "auditlog",
        component: AuditLog,
        name: "auditlog",
      },
      {
        path: "acknowledgement",
        component: AcknowledgementComp,
        name: "acknowledgement",
      },
      {
        path: "predefinedforms",
        component: PreDefineForms,
        name: "PredefinedForms",
      }
    ],
  },
];
export default settingRoutes;
