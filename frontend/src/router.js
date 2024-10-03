import { createRouter, createWebHistory } from "vue-router";
import RolesComp from "./Pages/RolesComp.vue";
import RolesMatrixes from "./Pages/RolesMatrixes.vue";
import WorkFlow from "./Pages/WorkFlow.vue";
const routes = [
  {
    path: "/Roles",
    name: RolesComp,
    component: RolesComp,
  },
  {
    path: "/RoleMatrix",
    name: RolesMatrixes,
    component: RolesMatrixes,
  },
  {
    path: "/Workflows",
    name: WorkFlow,
    component: WorkFlow,
  },
];

const router = createRouter({
  history: createWebHistory(),
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
