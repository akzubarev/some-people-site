import axios from "axios"
import Cookies from "js-cookie"

const request = axios.create({
  baseURL: "",
  timeout: 20000,
  headers: {
    "Content-Type": "application/json"
  }
})
request.interceptors.request.use(function(config) {
  const csrf = Cookies.get("csrftoken")
  if (csrf) {
    config.headers["X-CSRFToken"] = csrf
  }
  return config
})
export default request
