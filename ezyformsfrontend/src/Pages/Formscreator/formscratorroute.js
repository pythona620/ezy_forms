const FormsCreator = () => import("./FormsCreator.vue");
const Created = () => import("./CreatedComp.vue");
const Draft = () => import("./DraftComp.vue");

const Trash = () => import("./TrashComp.vue");
const FormStepper = () => import('./FormStepper.vue');

const createrRoutes = [
  {
    path: "/create-form",
    component: FormsCreator,
    redirect: "/create-form/created",

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
      // {
      //   path: "formsteps",
      //   component: FormStepper,
      //   name: "FormStepper"
      // },
      {
        path: 'formsteps/:paramid?',
        component: FormStepper,
        name: 'FormStepper'
      }
    ],
  },
];
export default createrRoutes;
