const ToDoComp = () => import("./ToDoComp.vue");
const MyTeam = () => import("./MyTeam.vue");
const RaisedByMe = () => import("./RaisedByMe.vue");
const HistoryComp = () => import("./HistoryComp.vue");
const ReceivedForMe = () => import("./ReceivedForMe.vue");
const todoroutes = [
  {
    path: "/todo",
    component: ToDoComp,
    redirect: "/todo/receivedform",

    children: [
      {
        path: "receivedform",
        component: ReceivedForMe,

        name: "ReceivedForMe",
      },
      {
        path: "history",
        component: HistoryComp,

        name: "HistoryComp",
      },
      {
        path: "raisedbyme",
        component: RaisedByMe,

        name: "RaisedByMe",
      },
      {
        path: "myteam",
        component: MyTeam,

        name: "MyTeam",
      },
    ],
  },
];
export default todoroutes;
