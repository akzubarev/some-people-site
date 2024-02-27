import store from "@/store"
import authService from "@/services/authService"
import { useRouter } from "vue-router"

export default async ({ next }) => {
  if (store.getters["auth/active"]) {
    try {
      if (store.getters["auth/user"] && store.getters["auth/user"].id) {
        authService.me().then(res => {
          if (res.data && res.data.id) {
            store.dispatch("auth/setUser", res.data)
          } else {
            store.dispatch("auth/setToken", null)
            const router = useRouter()
            router.push("/sign-in")
          }
        })
        return next()
      } else {
        const res = await authService.me()
        if (res.data && res.data.id) {
          store.dispatch("auth/setUser", res.data)
          return next()
        } else {
          store.dispatch("auth/setToken", null)
          return next("/sign-in")
        }
      }
    } catch (e) {
      store.dispatch("auth/setToken", null)
      return next("/sign-in")
    }
  } else {
    return next("/sign-in")
  }
}
