import axios from "axios"
import store from "@/store"

const request = axios.create({
    baseURL: "",
    timeout: 20000,
    headers: {
        "Content-Type": "application/json",
        // 'X-CSRFToken': {
        //   toString () {
        //     return Cookies.get('csrftoken')
        //   }
        // },
        Authorization: {
            toString() {
                const token = store.getters["auth/token"]
                if (token && token != "null") return "Token " + token
            }
        }
    }
    // validateStatus: function (status) {
    //   return status < 500
    // }
})
// request.interceptors.response.use(function (response) {
//     return response;
//   }, function (error) {
//     // log to sentry
//     if (error.response.status < 500)
//       return error.response
//     return Promise.reject(error)
//   });
export default request
