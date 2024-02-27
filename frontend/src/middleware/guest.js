import store from "@/store"

export default async ({ next }) => {
  if (!store.getters["auth/active"]) {
    next()
  } else {
    next("/")
  }
}
