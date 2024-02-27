import store from "@/store"
import walletService from "@/services/walletService"

export default async ({ next }) => {
  const data = (await walletService.subscriptionCount()).data
  return next()
}
