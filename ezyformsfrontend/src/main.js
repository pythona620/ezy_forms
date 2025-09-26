import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "../src/Styles/styles.scss";
import '@vueform/multiselect/themes/default.css';
import "vue3-toastify/dist/index.css";
 import Tooltip from 'primevue/tooltip';
// import PrimeVue from 'primevue/config';
// import Aura from '@primevue/themes/aura';
// import Tooltip from 'primevue/tooltip';
// import * as echarts from 'echarts';



const app = createApp(App);

app.use(router);
app.directive('tooltip', Tooltip);

// app.use(PrimeVue, {
//     theme: {
//         preset: Aura
//     }
// });
// app.use(PrimeVue, { ripple: true });
// app.directive('tooltip', Tooltip);
app.mount("#app");
const loader = document.getElementById("loader");
if (loader) {
  loader.style.transition = "opacity 0.3s ease";
  loader.style.opacity = 0;
  setTimeout(() => {
    loader.remove();
    // Show Vue app after loader is gone
    document.getElementById("app").style.visibility = "visible";
  }, 100);
}