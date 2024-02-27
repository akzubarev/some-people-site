import request from "@/services/request"

export default {
    async segment(name, uuid) {
        return await request.get(`/api/achieves/segment/` + name + "?uuid=" + uuid)
    },
    async list() {
        return await request.get(`/api/achieve_set/`)
    },
    async createAchieve(payload) {
        return await request.post(`/api/achieve_set/`, payload)
    },
    async make_lesson_watched(id) {
        return await request.get(`/api/lessons/make_watched?lesson_id=` + id)
    },
}
