import request from "@/services/request"

export default {
  async one(payload) {
    const response = await request.get(`/api/guides/` + payload + "/")
    return response
  },
  async list() {
    const response = await request.get(`/api/guides/?ordering=-id`)
    return response
  },
  async lessons(params) {
    if (params.tags) {
      params.tags = params.tags.join(",")
    }
    const response = await request.get("/api/lessons/", { params })
    // 	+
    //     (guide_id ? "&guide_id=" + guide_id : "") +
    //     (lessons_per_section
    //       ? "&lessons_per_section=" + lessons_per_section
    //       : "") +
    //     (section_id !== "" && section_id !== undefined
    //       ? "&section_id=" + section_id
    //       : "") +
    //     (tags.length > 0
    //       ? "&filter_faculty=" + tags.join(",")
    //       : "") +
    //     (webinars ? "&webinars=true" : "")
    return response
  },
  async lesson(lesson) {
    const response = await request.get(`/api/lessons/` + lesson + "/")
    return response
  }
}
