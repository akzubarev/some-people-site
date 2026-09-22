import {createApp} from "vue"
import App from "./App.vue"
import router from "./router"
import store from "./store"
import i18n from "@/i18n"

import {initInlineSvg} from "@/core/plugins/inline-svg"

const app = createApp(App)






app.use(store)
app.use(router)
app.use(i18n)

initInlineSvg(app)

app.mount("#app")
