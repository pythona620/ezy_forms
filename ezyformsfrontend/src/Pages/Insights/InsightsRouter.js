// Insights Module Routes

const InsightsMain = () => import('./InsightsMain.vue');
const FormsList = () => import('./FormsList.vue');
const FormRecords = () => import('./FormRecords.vue');
const DashboardBuilder = () => import('./DashboardBuilder.vue');
const DashboardView = () => import('./DashboardView.vue');
const DashboardList = () => import('./DashboardList.vue');

const insightsRoutes = [
  {
    path: '/insights',
    component: InsightsMain,
    meta: { LoginRequire: true, title: 'Insights - Ezy Forms' },
    redirect: '/insights/forms',
    children: [
      {
        path: 'forms',
        component: FormsList,
        name: 'InsightsForms',
        meta: { LoginRequire: true, title: 'Forms - Insights' }
      },
      {
        path: 'forms/:formName/records',
        component: FormRecords,
        name: 'FormRecords',
        meta: { LoginRequire: true, title: 'Form Records - Insights' },
        props: true
      },
      {
        path: 'dashboards',
        component: DashboardList,
        name: 'DashboardList',
        meta: { LoginRequire: true, title: 'Dashboards - Insights' }
      },
      {
        path: 'dashboards/create',
        component: DashboardBuilder,
        name: 'DashboardCreate',
        meta: { LoginRequire: true, title: 'Create Dashboard - Insights' },
        props: route => ({ formName: route.query.form })
      },
      {
        path: 'dashboards/:dashboardId/edit',
        component: DashboardBuilder,
        name: 'DashboardEdit',
        meta: { LoginRequire: true, title: 'Edit Dashboard - Insights' },
        props: true
      },
      {
        path: 'dashboards/:dashboardId/view',
        component: DashboardView,
        name: 'DashboardView',
        meta: { LoginRequire: true, title: 'View Dashboard - Insights' },
        props: true
      }
    ]
  }
];

export default insightsRoutes;
