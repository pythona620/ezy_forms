// routes.js


// Import necessary components
const MasterPage = () => import("./MasterPage.vue");
const AllDeptComp = () => import('./AllDepartment.vue');
const PreDefineForms = () => import('./PreDefineForms.vue');

// Define the Master routes
const Masterroutes = [
  {
    path: "/forms",
    component: MasterPage,
    redirect: "/forms/department/Allforms",
    children: [
      {
        path: 'department/:id',
        component: AllDeptComp,
        name: 'DepartmentDetail/:id',
        props: true, // Automatically pass route params as props
      },
      {
    path: "/forms/department/predefineForm",
    component: PreDefineForms,
    name: 'PreDefineForms',
    props: true, // Automatically pass route params as props
  }
    ],
  },
  
];

// Export the routes for use in the Vue Router
export default Masterroutes;
