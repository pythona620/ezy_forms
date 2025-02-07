import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "../src/Styles/styles.scss";
import '@vueform/multiselect/themes/default.css';
import "vue3-toastify/dist/index.css";
// import PrimeVue from 'primevue/config';
// import Aura from '@primevue/themes/aura';
// import Tooltip from 'primevue/tooltip';


const app = createApp(App);

app.use(router);
// app.use(PrimeVue, {
//     theme: {
//         preset: Aura
//     }
// });
// app.use(PrimeVue, { ripple: true });
// app.directive('tooltip', Tooltip);
app.mount("#app");
