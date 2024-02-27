// import store from "@/store"
import notificationService from "@/services/notificationService"

export default async ({ next }) => {
  const data = (await notificationService.telegram()).data

  if (data.chat_id) {
    return next()
  } else {
    // return next();
    return next("/account/telegram")
  }
}
