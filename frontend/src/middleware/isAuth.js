import store from "@/store"

export default async ({ next }) => {
  if (store.getters["auth/user"]) {
    return next()
  } else {
    return next("/sign-in")
  }
}
