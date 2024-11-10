import store from "@/store"
import authService from "@/services/authService"
// import gamesService from "../services/gamesService";

const _loadUser = async ({next}) => {
    try {
        const {data} = await authService.me()
        if (data && data.id) {
            store.dispatch('auth/setUser', data)
            return next()
        }
    } catch {
    }
    return next()
}

export const loadUser = async ({next}) => {
    if (!store.getters['auth/user']?.id) {
        return await _loadUser({next})
    } else {
        return next()
    }
}


// export const loadGame = async (id, {next}) => {
//     gamesService.game(id).then(({data}) => {
//         store.dispatch("setGame", data)
//         return next()
//     })
// }
