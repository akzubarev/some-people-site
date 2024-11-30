import request from "@/services/request"

export default {
    async game(alias) {
        return await request.get(`/api/games/${alias}/`)
    },
    async groups(game_alias) {
        return await request.get(`/api/games/groups/?game_alias=${game_alias}`)
    },
    async games(payload) {
        return await request.get(`/api/games/`, payload)
    },
    async characters(game_alias, search = null, tag = null) {
        const queryString = `game_alias=${game_alias}` +
            (!search ? '' : `&search=${search}`) +
            (!tag ? '' : `&tag=${tag}`)
        return await request.get(`/api/games/characters/?${queryString}`)
    },
    async application(user_id, game_alias) {
        return await request.get(`/api/applications/get/?user_id=${user_id}&game_alias=${game_alias}`)
    },
    async applications(user_id, game_alias = null) {
        const params = `user_id=${user_id}` + (game_alias ? `&game_alias=${game_alias}` : "")
        return await request.get(`/api/applications/?${params}`)
    },
    async apply(payload) {
        return await request.post(`/api/applications/apply/`, payload)
    },
    async delete_application(game_alias) {
        return await request.post(`/api/applications/delete/`, {game_alias: game_alias})
    },
    async restore_application(game_alias) {
        return await request.post(`/api/applications/restore/`, {game_alias: game_alias})
    },
    async questions(game_alias) {
        return await request.get(`/api/questions/?game_alias=${game_alias}`)
    },
    async tags(game_alias) {
        return await request.get(`/api/games/tags/?game_alias=${game_alias}`)
    },
    async likes(game_alias, character_id, like) {
        const payload = {game_alias: game_alias, character_id: character_id, like: like}
        return await request.get(`/api/users/likes/?game_alias=${game_alias}`, payload)
    },
    async like_character(game_alias, character_id, like) {
        const payload = {game_alias: game_alias, character_id: character_id, like: like}
        return await request.post(`/api/users/like_character/`, payload)
    },
}
