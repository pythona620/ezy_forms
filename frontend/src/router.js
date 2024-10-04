import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from "vue-router";
import Masterroutes from "./Pages/Master/Masterroutes";

const routes = [...Masterroutes];

const router = createRouter({
  history: createWebHashHistory("/frontend"),
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
