import request from "@/services/request"

export default {
    async mg() {
        return await request.get(`/api/users/mg/`)
    },
}
