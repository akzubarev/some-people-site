import store from "@/store"
import authService from "@/services/authService"
import gamesService from "../services/gamesService";
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
    if (!store.getters['auth/user']?.id)
        return await _loadUser({next})
    else
        return next()
}


export const loadGames = async ({next}) => {
    if (!Object.keys(store.getters['games/games']).length) {
        const response = await gamesService.games()
        const games = {}
        response.data.forEach(game => (games[game.alias] = game))
        store.dispatch("games/setGames", games)
    } else {
        // gamesService.games().then(({data}) => {
        //     const games = {}
        //     data.forEach(game => (games[game.alias] = game))
        //     store.dispatch("games/setGames", games)
        // })
    }
    return next()
}

export const loadApplication = async ({next}) => {
    if (!Object.keys(store.getters['games/games']).length) {
        const applicationData = await gamesService.application(store.getters['auth/user'].id, 'whales')
        store.dispatch("games/setApplication", applicationData.data)
        const questionsData = await gamesService.questions('whales')
        store.dispatch("games/setQuestions", questionsData.data)
    }
    return next()
}