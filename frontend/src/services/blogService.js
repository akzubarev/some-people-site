import request from "@/services/request"

export default {
  async post(id) {
    return await request.get(`/api/blog/${id}/`)
  },
  async list(payload) {
    return await request.get(`/api/blog/`, payload)
  }
}
