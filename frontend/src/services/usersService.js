import request from "@/services/request"

export default {
    async get(user_id) {
        return await request.get(`/api/users/${user_id}/`)
    },
    async list() {
        return await request.get(`/api/users/`)
    },
    async players(game_alias) {
        return await request.get(`/api/users/players?game_alias=${game_alias}`)
    },
    async mg() {
        return await request.get(`/api/users/mg/`)
    },
}
