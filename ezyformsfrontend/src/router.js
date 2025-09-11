import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from "vue-router";
import Masterroutes from "./Pages/Forms/Masterroutes";
import settingRoutes from "./Pages/Settings/settingroutes";
import todoroutes from "./Pages/ToDo/todoroute";
import createrRoutes from "./Pages/Formscreator/formscratorroute";
import archivedroutes from "./Pages/Archived/archivedroutes";
import dashBoardroutes from "./Pages/Dashboard/dashboardroute";
import Login from "./views/Login.vue";
import isAuthenticated from "../src/shared/services/auth";
import RaiseRequest from './Components/RaiseRequest.vue';
import NotFound from './Components/NotFound.vue'
import ApproveRequest from "./Components/ApproveRequest.vue";
import FormPreview from "./Components/FormPreview.vue";
import FormPreviewComp from "./Components/FormPreviewComp.vue";
import PdfPreview from "./Components/PdfPreview.vue";
import EmailApprove from "./Components/EmailApprove.vue";
import LinkPreviewComp from "./Components/LinkPreviewComp.vue";
import WorkOrderDetailes from "./Components/WorkOrderDetailes.vue";
// import QrRaiseRequest from "./Components/QrRaiseRequest.vue";
import EmployeeForms from "./Components/EmployeeForms.vue";


const routes = [
  {
    path: '/',
    component: Login,
    name: 'LoginPage'
  },
  ...Masterroutes,
  ...settingRoutes,
  ...todoroutes,
  ...createrRoutes,
  ...archivedroutes,
  ...dashBoardroutes,
  {
    path: '/raiserequest',
    component: RaiseRequest,
    name: 'RaiseRequest'
  },
  {
    path: '/approverequest',
    component: ApproveRequest,
    name: 'ApproveRequest'
  },
  {
    path: '/emailapprove',
    component: EmailApprove,
    name: 'EmailApprove',
  },
  // {
  //   path: '/qrraiserequest',
  //   component: QrRaiseRequest,
  //   name: 'QrRaiseRequest',
  // },
  {
    path: '/formpreview',
    component: FormPreview,
    name: 'FormPreview'
  },
  {
    path: '/formpreviewComp',
    component: FormPreviewComp,
    name: 'FormPreviewComp'
  },
  {
    path: '/linkpreviewComp',
    component: LinkPreviewComp,
    name: 'LinkPreviewComp'
  },
  {
    path: '/pdfpreview',
    component: PdfPreview,
    name: 'PdfPreview'
  },
   {
    path: '/employeeforms',
    component: EmployeeForms,
    name: 'employeeforms'
  },
  {
    path:'/settings/vendorcomparison',
    component:WorkOrderDetailes,
    name:'vendorcomparison'
  },

  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const router = createRouter({
  history: createWebHashHistory("/ezyformsfrontend/"),
  routes,
});
router.beforeEach((to, from, next) => {
  const isLoggedIn = isAuthenticated();  // Check if the user is authenticated
  const requiresAuth = to.matched.some((record) => record.meta?.LoginRequire);

  // Allow access to /approverequest without login
  if (to.name === 'EmailApprove') {
    next(); // Skip authentication for this route
  }
  // if (to.name === 'QrRaiseRequest') {
  //   next();
  // }
  // If the route requires authentication and the user is not logged in, redirect to LoginPage
  else if (requiresAuth && !isLoggedIn) {
    next({ name: 'LoginPage' });
  }
  // If the user is logged in and tries to access LoginPage, redirect to DashBoard
  else if (isLoggedIn && to.name === 'LoginPage') {
    next({ path: '/dashboard/maindash' });
  }
  // If the user is not logged in and tries to access any protected route, redirect to LoginPage
  else if (!isLoggedIn && to.name !== 'LoginPage') {
    next({ name: 'LoginPage' });
  }
  // For all other cases, proceed normally
  else {
    next();
  }
});

// router.beforeEach((to, from, next) => {
//   to.matched.forEach(record => {
//     if (typeof record.meta.breadcrumb === 'function') {
//       record.meta.breadcrumb = record.meta.breadcrumb(to);
//     }
//   });
//   next();
// });
export default router;
