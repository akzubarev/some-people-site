import store from "@/store"
import authService from "@/services/authService"
import gamesService from "../services/gamesService";
import {default_games} from "../constants/defaults";

const _loadUser = async ({next}) => {

}

export const loadUser = async ({next}) => {
    if (!store.getters['auth/user']?.id)
        await authService.me().then(({data}) => {
            if (data && data.id)
                store.dispatch('auth/setUser', data)
        })
    return next()
}

export const forceLoadUser = async ({next}) => {
    if (!store.getters['auth/user']?.id)
        try {
            const {data} = await authService.me()
            if (data && data.id)
                store.dispatch('auth/setUser', data)
        } catch {
        }
    return next()
}


export const loadGames = async ({next}) => {
    if (!Object.keys(store.getters['games/games']).length)
        store.dispatch("games/setGames", default_games)
    gamesService.games().then(({data}) => {
        const games = {}
        data.forEach(game => (games[game.alias] = game))
        store.dispatch("games/setGames", games)
    })
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
export const loadQuestions = async ({next}) => {
    gamesService.questions('whales').then(({data}) => {
        store.dispatch("games/setQuestions", data)
    })
    return next()
}