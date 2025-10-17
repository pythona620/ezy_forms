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
        meta: { title: 'Created Forms - Ezy Forms' }
      },
      {
        path: "trash",
        component: Trash,
        name: "Trash",
        meta: { title: 'Trash - Ezy Forms' }
      },
      {
        path: "draft",
        component: Draft,
        name: "Draft",
        meta: { title: 'Drafts - Ezy Forms' }
      },
      // {
      //   path: "formsteps",
      //   component: FormStepper,
      //   name: "FormStepper"
      // },
      {
        path: 'formsteps/:paramid?',
        component: FormStepper,
        name: 'FormStepper',
        meta: { title: 'Form Creation - Ezy Forms'}
      }
    ],
  },
];
export default createrRoutes;
