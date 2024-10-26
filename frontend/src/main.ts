import {createApp} from "vue"
import App from "./App.vue"
// import Cookies from "js-cookie"
import router from "./router"
import store from "./store"
import i18n from "@/i18n"

import {initInlineSvg} from "@/core/plugins/inline-svg"

import "bootstrap"

const app = createApp(App)

import VueAwesomePaginate from "vue-awesome-paginate"

// import the necessary css file
import "vue-awesome-paginate/dist/style.css"

app.use(VueAwesomePaginate)

app.use(store)
app.use(router)
app.use(i18n)

initInlineSvg(app)

app.mount("#app")
