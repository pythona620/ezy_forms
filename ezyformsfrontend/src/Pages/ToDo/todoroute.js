

const ToDoComp = () => import("./ToDoComp.vue");
const MyTeam = () => import("./MyTeam.vue");
const RaisedByMe = () => import("./RaisedByMe.vue");
const HistoryComp = () => import("./HistoryComp.vue");
const ReceivedForMe = () => import("./ReceivedForMe.vue");
const ReportsComp = () => import("./ReportsComp.vue");
const InsightsComp = () => import("./InsightsComp.vue");

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
        meta: { title: 'Assign To Me - Ezy Forms' }
      },
      {
        path: "history",
        component: HistoryComp,

        name: "HistoryComp",
        meta: { title: 'My Approvals - Ezy Forms' }
      },
      {
        path: "raisedbyme",
        component: RaisedByMe,

        name: "RaisedByMe",
        meta: { title: 'My Requests - Ezy Forms' }
      },
      {
        path: "myteam",
        component: MyTeam,

        name: "MyTeam",
        meta: { title: 'My Team Requests- Ezy Forms' }
      },
      {
        path: "reports",
        component: ReportsComp,
        name: "ReportsComp",
        meta: { title: 'Reports - Ezy Forms' }
      },
      {
        path: "insights",
        component: InsightsComp,
        name: "InsightsComp",
        meta: { title: 'Insights - Ezy Forms' }
      },
    ],
  },
];
export default todoroutes;
