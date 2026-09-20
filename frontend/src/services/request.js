import axios from "axios"
import store from "@/store"
import {sessionVersion} from './sessionVersion'

const request = axios.create({
    baseURL: "",
    timeout: 20000,
    headers: {
        "Content-Type": "application/json",
        Authorization: {
            toString() {
                const token = store.getters["auth/token"]
                if (token && token != "null") return "Token " + token
            }
        }
    }
})
request.interceptors.request.use(config => {
    config.sessionVersion = sessionVersion()
    return config
})
request.interceptors.response.use(response => {
    if (!response.config.skipSessionGuard && response.config.sessionVersion !== sessionVersion()) {
        return Promise.reject(new axios.Cancel('Session changed while request was pending'))
    }
    return response
}, error => {
    if (error.config && !error.config.skipSessionGuard && error.config.sessionVersion !== sessionVersion()) {
        return Promise.reject(new axios.Cancel('Session changed while request was pending'))
    }
    return Promise.reject(error)
})
export default request
