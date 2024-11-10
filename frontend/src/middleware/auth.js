import store from "@/store"

export const guest = async ({next}) => {
    next()
}

export const isAuth = async ({next}) => {
    if (!!store.getters['auth/user']?.id) {
        return next()
    } else {
        return next('/sign-in')
    }
}

export const isMg = async ({next}) => {
    if (store.getters['auth/user']?.mg) {
        return next()
    } else {
        return next("/")
    }
}
