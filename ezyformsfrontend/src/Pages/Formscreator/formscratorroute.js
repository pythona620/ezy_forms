const FormsCreator = () => import("./FormsCreator.vue");
const Created = () => import("./CreatedComp.vue");
const Draft = () => import("./DraftComp.vue");

const Trash = () => import("./TrashComp.vue");

const createrRoutes = [
  {
    path: "/new",
    component: FormsCreator,
    redirect: "/new/created",

    children: [
      {
        path: "created",
        component: Created,
        name: "Created",
      },
      {
        path: "trash",
        component: Trash,
        name: "Trash",
      },
      {
        path: "draft",
        component: Draft,
        name: "Draft",
      },
    ],
  },
];
export default createrRoutes;
