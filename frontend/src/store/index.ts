import { createStore } from "vuex"
import { config } from "vuex-module-decorators"
import { ref, readonly } from "vue"
import auth from './modules/auth'
import body from './modules/body'
import games from './modules/games'

config.rawError = true

const modules: Record<string, any> = {auth, body, games}
Object.values(modules).forEach(module => { module.namespaced = true })

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

export const navigationPending = ref(true)
