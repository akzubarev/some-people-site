import { createI18n } from "vue-i18n"
import Cookies from "js-cookie"

// const requireContext = require.context("./locales", false, /.*\.json$/)
const requireContext = require.context("./locales", false, /.*\.js$/)

const removeEmpty = obj => (Object.entries(obj)
    .filter(([_, v]) => v !== "")
    .reduce(
      (acc, [k, v]) => ({ ...acc, [k]: v === Object(v) ? removeEmpty(v) : v }),
      {}
    )
)

const messages = requireContext
  .keys()
  // .filter(file => file.search(".json") !== -1)
  // .map(file => [file.replace(/(^.\/)|(\.json$)/g, ""), requireContext(file)])
  .filter(file => file.search(".js") !== -1)
  .map(file => [file.replace(/(^.\/)|(\.js$)/g, ""), requireContext(file)])
  .reduce((modules, [name, module]) => {
    if (module.default) {
      module = module.default
    }
    module = removeEmpty(module)
    return { ...modules, [name]: module }
  }, {})

const lang = 'ru';
Cookies.set("django_language", lang, { expires: 30 })
const i18n = createI18n({
  legacy: false,
  locale: lang,
  globalInjection: true,
  fallbackLocale: "ru",
  messages
})
// console.log(i18n.t)
// console.log(i18n.locale);
export default i18n
