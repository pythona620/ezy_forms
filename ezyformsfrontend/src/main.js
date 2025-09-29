import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "../src/Styles/styles.scss";
import '@vueform/multiselect/themes/default.css';
// import "vue3-toastify/dist/index.css";
 import Tooltip from 'primevue/tooltip';
// import PrimeVue from 'primevue/config';
// import Aura from '@primevue/themes/aura';
// import Tooltip from 'primevue/tooltip';
// import * as echarts from 'echarts';
import Toast, { POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";


const app = createApp(App);

app.use(router);
app.directive('tooltip', Tooltip);
app.use(Toast, {
  position: POSITION.TOP_RIGHT,
  timeout: 2000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
});

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