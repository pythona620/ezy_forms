const DashBoard = () => import("./DashBoard.vue");
const MainDashBoard = () => import("./DashBoardComp.vue");
const dashBoardroutes = [
  {
    path: "/dashboard",
    component: DashBoard,
    redirect: "/dashboard/maindash",
    children: [
      {
        path: "maindash",
        component: MainDashBoard,
        name: MainDashBoard,
      },
    ],
  },
];
export default dashBoardroutes;
