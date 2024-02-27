import { ref } from "vue"
// import Swal from "sweetalert2/dist/sweetalert2.min.js"
import { useStore } from "vuex"

export default () => {
  const fieldsPages = ref(null)
  const errors = ref({})
  const data = ref({})
  // const popup = Swal
  const currentPage = ref(0)

  const store = useStore()

  const errorHandler = async () => {
    popup.close()
    let msg
    if (data.value["detail"]) {
      msg = data.value["detail"]
    }
    if (typeof data.value == "object" && data.value[0]) {
      msg = data.value[0]
    }
    if (data.value["non_field_errors"]) {
      msg = data.value["non_field_errors"][0]
    }
    if (msg) {
      // Swal.fire({
      //   text: msg,
      //   icon: "error",
      //   buttonsStyling: false,
      //   confirmButtonText: "OK",
      //   customClass: {
      //     confirmButton: "btn fw-bold btn-light-danger"
      //   }
      // })
      return
    }
    let minPageError = undefined
    if (data.value) {
      const errorsTmp = data.value
      let key
      for (key in errorsTmp) {
        if (Array.isArray(errorsTmp[key])) errorsTmp[key] = errorsTmp[key][0]
        if (fieldsPages.value !== null) {
          let page
          for (page in fieldsPages.value) {
            if (
              fieldsPages.value[page].includes(key) &&
              (minPageError == undefined || page < minPageError)
            ) {
              minPageError = page
            }
          }
        }
      }
      if (minPageError !== undefined && currentPage.value !== undefined) {
        currentPage.value = +minPageError
      }
      errors.value = errorsTmp
    }
  }
  const send = async dataHandler => {
    // popup.showLoading()
    store.dispatch("body/showActionLoader")
    data.value = {}
    errors.value = {}
    try {
      await dataHandler()
      // popup.close()
      store.dispatch("body/hideActionLoader")
      return true
    } catch (e) {
      store.dispatch("body/hideActionLoader")
      console.log(e);
      data.value = {}
      try {
        data.value = e.response.data
      } catch (e) {
        data.value["detail"] =
          'Internal error. Please, try again later.' +
          (data.value["detail"] || "")
      }
      await errorHandler()
      return false
    }
  }
  return {
    errors,
    fieldsPages,
    currentPage,
    send
  }
}
