import { createStore } from "vuex"
import { config } from "vuex-module-decorators"
import { ref, readonly } from "vue"
// import AuthModule from "@/store/modules/AuthModule";
// import BodyModule from "@/store/modules/BodyModule";
// import BreadcrumbsModule from "@/store/modules/BreadcrumbsModule";
// import ConfigModule from "@/store/modules/ConfigModule";

config.rawError = true

const requireContext = require.context("./modules", false, /.*\.ts$/)

const modules = requireContext
  .keys()
  .filter(file => file.search(".ts") !== -1)
  .map(file => [file.replace(/(^.\/)|(\.ts$)/g, ""), requireContext(file)])
  .reduce((modules, [name, module]) => {
    if (module.default) {
      module = module.default
    }
    if (module.namespaced === undefined) {
      module.namespaced = true
    }
    return { ...modules, [name]: module }
  }, {})

const store = createStore({
  modules
})

export default store

const _title = ref("")
const _metaData = ref({})
export const pageTitle = readonly(_title)
export const metaData = readonly(_metaData)

export const setPageTitle = v => (_title.value = v)
export const setMetaData = v => (_metaData.value = v)
export const updateMetaData = v =>
  (_metaData.value = Object.assign({}, _metaData.value, v))
