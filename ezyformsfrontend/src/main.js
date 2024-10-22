import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "../src/Styles/styles.scss";
import '@vueform/multiselect/themes/default.css';



const app = createApp(App);

app.use(router);
app.mount("#app");
