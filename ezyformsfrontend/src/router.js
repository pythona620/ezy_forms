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
const routes = [
  ...Masterroutes,
  ...settingRoutes,
  ...todoroutes,
  ...createrRoutes,
  ...archivedroutes,
  ...dashBoardroutes,
];

const router = createRouter({
  history: createWebHashHistory("/ezyformsfrontend"),
  routes,
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
