import request from "@/services/request"

export default {
    async players(game_alias) {
        return await request.get(`/api/users/players?game_alias=${game_alias}`)
    },
    async mg() {
        return await request.get(`/api/users/mg/`)
    },
}
