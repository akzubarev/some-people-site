import { computed } from "vue"
import store from "@/store/index"

/**
 * Returns layout config
 * @returns {object}
 */
export const config = computed(() => {
  return store.getters["config/layoutConfig"]()
})

/**
 * Set the sidebar display
 * @returns {boolean}
 */
export const displaySidebar = computed(() => {
  return store.getters["config/layoutConfig"]("sidebar.display")
})

/**
 * Check if footer container is fluid
 * @returns {boolean}
 */
export const footerWidthFluid = computed(() => {
  return store.getters["config/layoutConfig"]("footer.width") === "fluid"
})

/**
 * Check if header container is fluid
 * @returns {boolean}
 */
export const headerWidthFluid = computed(() => {
  return store.getters["config/layoutConfig"]("header.width") === "fluid"
})

/**
 * Returns header left part type
 * @returns {string}
 */
export const headerLeft = computed(() => {
  return store.getters["config/layoutConfig"]("header.left")
})

export const headerDark = computed(() => {
  return store.getters["config/layoutConfig"]("header.theme") == "dark"
})
/**
 * Set the aside display
 * @returns {boolean}
 */
export const asideDisplay = computed(() => {
  return store.getters["config/layoutConfig"]("aside.display") === true
})

/**
 * Check if toolbar width is fluid
 * @returns {boolean}
 */
export const toolbarWidthFluid = computed(() => {
  return store.getters["config/layoutConfig"]("toolbar.width") === "fluid"
})

/**
 * Set the toolbar display
 * @returns {boolean}
 */
export const toolbarDisplay = computed(() => {
  return store.getters["config/layoutConfig"]("toolbar.display")
})

/**
 * Check if the page loader is enabled
 * @returns {boolean}
 */
export const loaderEnabled = computed(() => {
  return store.getters["config/layoutConfig"]("loader.display")
})

/**
 * Check if container width is fluid
 * @returns {boolean}
 */
export const contentWidthFluid = computed(() => {
  return store.getters["config/layoutConfig"]("content.width") === "fluid"
})

/**
 * Page loader logo image
 * @returns {string}
 */
export const loaderLogo = computed(() => {
  return (
    process.env.BASE_URL + store.getters["config/layoutConfig"]("loader.logo")
  )
})

/**
 * Check if the aside menu is enabled
 * @returns {boolean}
 */
export const asideEnabled = computed(() => {
  return !!store.getters["config/layoutConfig"]("aside.display")
})

/**
 * Set the aside theme
 * @returns {string}
 */
export const asideTheme = computed(() => {
  return store.getters["config/layoutConfig"]("aside.theme")
})

/**
 * Set the subheader display
 * @returns {boolean}
 */
export const subheaderDisplay = computed(() => {
  return store.getters["config/layoutConfig"]("toolbar.display")
})

/**
 * Set the aside menu icon type
 * @returns {string}
 */
export const asideMenuIcons = computed(() => {
  return store.getters["config/layoutConfig"]("aside.menuIcon")
})

/**
 * Light theme logo image
 * @returns {string}
 */
export const themeLightLogo = computed(() => {
  return (
    process.env.BASE_URL +
    store.getters["config/layoutConfig"]("main.logo.light")
  )
})

/**
 * Dark theme logo image
 * @returns {string}
 */
export const themeDarkLogo = computed(() => {
  return (
    process.env.BASE_URL +
    store.getters["config/layoutConfig"]("main.logo.dark")
  )
})

/**
 * Set the header menu icon type
 * @returns {string}
 */
export const headerMenuIcons = computed(() => {
  return store.getters["config/layoutConfig"]("header.menuIcon")
})
