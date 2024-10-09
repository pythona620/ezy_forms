const MainPage = () => import("./MainComp.vue");
const ArchivedComp = () => import("./ArchivedComp.vue");
const archivedroutes = [
  {
    path: "/archived",
    component: MainPage,
    redirect: "/archived/mainarchive",

    children: [
      {
        path: "mainarchive",
        component: ArchivedComp,

        name: "ArchivedComp",
      },
    ],
  },
];
export default archivedroutes;
