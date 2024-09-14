import store from "@/store"
import authService from "@/services/authService"
// import {useRouter} from "vue-router"

const _loadUser = async ({next}) => {
    try {
        authService.me().then(res => {
            if (res.data && res.data.id) {
                store.dispatch("auth/setUser", res.data)
            } else {
                store.dispatch("auth/setToken", null)
                // const router = useRouter()
                // router.push("/sign-in")
            }
        })
    } catch (e) {
        store.dispatch("auth/setToken", null)
        // return next("/sign-in")
    }
    return next()
}

export const loadUser = async ({next}) => {
    if (store.getters["auth/active"]) {
        return await _loadUser({next})
    } else {
        // return next("/sign-in")
        return next()
    }
}

export const forceLoadUser = async ({next}) => {
    return await _loadUser({next})
}
