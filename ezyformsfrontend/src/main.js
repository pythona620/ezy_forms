import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "../src/Styles/styles.scss";
import '@vueform/multiselect/themes/default.css';
import "vue3-toastify/dist/index.css";
import * as echarts from 'echarts';



const app = createApp(App);

app.use(router);
app.mount("#app");
