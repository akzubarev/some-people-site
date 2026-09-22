import { ref } from "vue"

export default () => {
  const fieldsPages = ref(null)
  const errors = ref({})
  const data = ref({})
  const currentPage = ref(0)


  const errorHandler = async () => {
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
    data.value = {}
    errors.value = {}
    try {
      await dataHandler()
      return true
    } catch (e) {
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
