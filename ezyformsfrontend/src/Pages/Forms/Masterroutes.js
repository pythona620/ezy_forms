// routes.js

// Import necessary components
const MasterPage = () => import("./MasterPage.vue");
const AllDeptComp = () => import('./AllDepartment.vue');

// Define the Master routes
const Masterroutes = [
  {
    path: "/forms",
    component: MasterPage,
    redirect: "/forms/department/:id",
    children: [
      {
        path: 'department/:id',
        component: AllDeptComp,
        name: 'DepartmentDetail',
        props: true, // Automatically pass route params as props
      },
    ],
  },
];

// Export the routes for use in the Vue Router
export default Masterroutes;
