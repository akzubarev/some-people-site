import store from '@/store'
import axios from 'axios'
import authService from '@/services/authService'
import gamesService from '@/services/gamesService'

let gamesRequest = 0
let accountRequest = 0

export const loadUser = async ({next}) => {
    if (!store.getters['auth/user']?.id) {
        try {
            const {data} = await authService.me()
            if (data?.id) await store.dispatch('auth/setUser', data)
        } catch (error) {
            if (!axios.isCancel(error)) await store.dispatch('auth/logout')
        }
    }
    return next()
}

export const loadGames = async ({to, next}) => {
    const request = ++gamesRequest
    store.commit('games/SET_GAMES_ERROR', '')
    try {
        const {data} = await gamesService.games()
        if (request !== gamesRequest) return next(false)
        if (!Array.isArray(data)) throw new Error('Invalid games response')
        const games = Object.fromEntries(data.map(game => [game.alias, game]))
        store.commit('games/SET_GAMES', games)
        if (to.params.game_alias && !games[to.params.game_alias]) return next('/404')
    } catch (error) {
        if (request !== gamesRequest || axios.isCancel(error)) return next(false)
        store.commit('games/SET_GAMES', {})
        store.commit('games/SET_GAMES_ERROR', 'Не удалось загрузить игры. Попробуйте ещё раз.')
    }
    return next()
}

export const loadAccount = async ({to, next}) => {
    const request = ++accountRequest
    store.commit('games/SET_APPLICATION', {})
    store.commit('games/SET_QUESTIONS', [])
    store.commit('games/SET_ACCOUNT_ERROR', '')
    const alias = to.params.game_alias
    store.commit('games/SET_ACCOUNT_ALIAS', alias || '')
    if (!alias || store.state.games.gamesError) return next()
    try {
        const [application, questions] = await Promise.all([
            gamesService.application(alias), gamesService.questions(alias),
        ])
        if (request !== accountRequest) return next(false)
        if (!application.data || Array.isArray(application.data) || !Array.isArray(questions.data)) {
            throw new Error('Invalid account response')
        }
        store.commit('games/SET_APPLICATION', application.data)
        store.commit('games/SET_QUESTIONS', questions.data)
    } catch (error) {
        if (request !== accountRequest || axios.isCancel(error)) return next(false)
        store.commit('games/SET_ACCOUNT_ERROR', 'Не удалось загрузить заявку. Попробуйте ещё раз.')
    }
    return next()
}
