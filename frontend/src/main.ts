import { createApp } from "vue"
import App from "./App.vue"
import Cookies from "js-cookie"
/*
TIP: To get started with clean router change path to @/router/clean.ts.
 */
import router from "./router"
import store from "./store"
// import ElementPlus from "element-plus";
import i18n from "@/i18n"

import { initInlineSvg } from "@/core/plugins/inline-svg"

import "bootstrap"

const app = createApp(App)

import VueAwesomePaginate from "vue-awesome-paginate"

// import the necessary css file
import "vue-awesome-paginate/dist/style.css"
app.use(VueAwesomePaginate)

app.use(store)
app.use(router)
// app.use(ElementPlus);
// app.use(Particles)

// MockAdapter.init(app);
// initApexCharts(app);
initInlineSvg(app)
// initVeeValidate();

app.use(i18n)

app.mount("#app")
