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
const WorkOrder = ()=>import("./WorkOrder.vue")
const PasswordPolicy=()=>import("./PasswordPolicy.vue");
const EmailQueue=()=>import("./EmailQueue.vue")

const EmailTemplate=()=>import("./EmailTemplate.vue");

const settingRoutes = [
  {
    path: "/settings",
    component: SettingsPage,
    redirect: "/settings/profile",
    meta: { title: 'Settings - Ezy Forms' },

    children: [
      {
        path: "employee",
        component: EmployeeComp,
        name: "EmployeeComp",
        meta: { title: 'Employee Management - Ezy Forms' }
      },
      {
        path: "inactiveEmployee",
        component: InactiveEmployee,
        name: "InactiveEmployee",
        meta: { title: 'Inactive Employee - Ezy Forms' }
      },
      {
        path: "employeeapproval",
        component: WebEmployee,
        name: "WebEmployee",
        meta: { title: 'Employee Approval - Ezy Forms' }
      },
      {
        path: "profile",
        component: ProfileComp,
        name: "ProfileComp",
        meta: { title: 'Profile - Ezy Forms' }
      },
      {
        path: "notifications",
        component: NotificationComp,
        name: "NotificationComp",
        meta: { title: 'Notifications - Ezy Forms' }
      },
      {
        path: "workflow",
        component: WorkFLow,
        name: "WorkFLow",
        meta: { title: 'Workflow - Ezy Forms' }
      },
      {
        path: "role",
        component: Roles,
        name: "Roles",
        meta: { title: 'Roles - Ezy Forms' }
      },
      {
        path: "rolematrix",
        component: RolesMatrix,
        name: "RolesMatrix",
        meta: { title: 'Role Matrix - Ezy Forms' }
      },

      {
        path: "categories",
        component: Categories,
        name: "Categories",
        meta: { title: 'Categories - Ezy Forms' }
      },
      {
        path: "designations",
        component: Designations,
        name: "Designations",
        meta: { title: 'Designations - Ezy Forms' }
      },
      {
        path: "department",
        component: DepartmentComp,
        name: "DepartmentComp",
        meta: { title: 'Department - Ezy Forms' }
      },
      {
        path: "esign",
        component: EsignComp,
        name: "EsignComp",
        meta: { title: 'E-Sign - Ezy Forms' }
      },
      {
        path: "authenticationpage",
        component: AuthenticationPage,
        name: "authenticationpage",
        meta: { title: 'Authentication - Ezy Forms' }
      },
      {
        path: "activitylog",
        component: ActivityLog,
        name: "ActivityLog",
        meta: { title: 'Activity Log - Ezy Forms' }
      },
      {
        path: "CreateForm",
        component: CreateForm,
        name: "CreateForm",
        meta: { title: 'Form Creation - Ezy Forms' }
      },
      {
        path: "auditlog",
        component: AuditLog,
        name: "auditlog",
        meta: { title: 'Audit Log - Ezy Forms' }
      },
      {
        path: "acknowledgement",
        component: AcknowledgementComp,
        name: "acknowledgement",
        meta: { title: 'Acknowledgement - Ezy Forms' }
      },
      {
        path: "predefinedforms",
        component: PreDefineForms,
        name: "PredefinedForms",
        meta: { title: 'Form Templates- Ezy Forms' }
      },
      {
        path:"workorder",
        component:WorkOrder,
        name:"workorder",
        meta: { title: 'Work Order - Ezy Forms' }
      },
      {
      
        path: "emailtemplate",
        component: EmailTemplate,
        name: "emailtemplate",
        meta: { title: 'Email Template - Ezy Forms' }
      },
       {
        path:"passwordpolicy",
        component:PasswordPolicy,
        name:"passwordpolicy",
        meta: { title: 'Password Policy - Ezy Forms' }
      },
      {
        path: "emailqueue",
        component: EmailQueue,
        name: "emailqueue",
        meta: { title: 'Email Queue - Ezy Forms' }
      },
    ],
  },
];
export default settingRoutes;
