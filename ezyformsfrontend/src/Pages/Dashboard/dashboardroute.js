const DashBoard = () => import("./DashBoard.vue");
const MainDashBoard = () => import("./DashBoardComp.vue");
const NewDashboard = () => import("./NewDashboard.vue");
const dashBoardroutes = [
  {
    path: "/dashboard",
    component: DashBoard,
    redirect: "/dashboard/maindash",
    meta:{ title: 'Dashboard - Ezy Forms' },
    children: [
      {
        path: "maindash",
        component: MainDashBoard,
        name: MainDashBoard,
      },
      {
        path: "insights",
        component: NewDashboard,
        name: "InsightsDashboard",
        meta: { title: 'Insights Dashboard - Ezy Forms', LoginRequire: true }
      },
    ],
  },
];
export default dashBoardroutes;
