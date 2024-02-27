import store from "@/store"

export default async ({ next }) => {
  if (store.getters["auth/active"]) {
    return next()
  } else {
    return next("/sign-in")
  }
}
