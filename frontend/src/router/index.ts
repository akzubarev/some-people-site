import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router"
import store from "@/store"
import {Mutations} from "@/store/enums/StoreEnums"
import isAuth from "@/middleware/isAuth"
import guest from "@/middleware/guest"
import loadUser from "@/middleware/loadUser"
import {setPageTitle} from "@/store"
import Layout from "@/layout/Layout.vue"

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        redirect: "/dashboard",
        component: Layout,
        children: [
            {
                path: "/dashboard",
                name: "dashboard",
                component: () => import("@/views/dashboard/Dashboard.vue"),
                meta: {
                    // middleware: [isAuth, loadUser]
                }
            },
            {
                path: "/mg",
                name: "mg",
                component: () => import("@/views/dashboard/MG.vue"),
                meta: {
                    // middleware: [isAuth, loadUser]
                }
            },
            {
                path: "/account/profile",
                name: "account-profile",
                component: () => import("@/views/account/Profile.vue"),
                meta: {
                    middleware: [isAuth, loadUser]
                }
            },
            {
                path: "/account",
                name: "account",
                redirect: "/account/profile",
                component: () => import("@/views/account/Account.vue"),
                children: [
                    {
                        path: "telegram",
                        name: "account-telegram",
                        component: () => import("@/views/account/Telegram.vue"),
                        meta: {
                            middleware: [isAuth, loadUser]
                        }
                    },
                    {
                        path: "settings",
                        name: "account-settings",
                        component: () => import("@/views/account/Settings.vue"),
                        meta: {
                            middleware: [isAuth, loadUser]
                        }
                    },
                    {
                        path: "notifications",
                        name: "account-notifications",
                        component: () => import("@/views/account/Notifications.vue"),
                        meta: {
                            middleware: [isAuth, loadUser]
                        }
                    }
                ]
            },
            {
                path: "/games",
                name: "games",
                component: () => import("@/views/games/Games.vue"),
                meta: {
                    // middleware: [loadUser]
                }
            },
            {
                path: "/game/:alias",
                name: "game",
                redirect: "/game/:alias/about",
                component: () => import("@/views/games/game/GameRoot.vue"),
                props: true,
                children: [
                    {
                        path: "/game/:alias/about",
                        name: "game-about",
                        component: () => import("@/views/games/game/About.vue"),
                        props: true,
                        meta: {
                            // middleware: [loadUser]
                        }
                    },
                    {
                        path: "/game/:alias/roles",
                        name: "game-roles",
                        component: () => import("@/views/games/game/Roles.vue"),
                        props: true,
                        meta: {
                            // middleware: [loadUser]
                        }
                    },
                    {
                        path: "/game/:alias/characters",
                        name: "game-characters",
                        component: () => import("@/views/games/game/CharacterList.vue"),
                        props: true,
                        meta: {
                            // middleware: [loadUser]
                        }
                    },
                    {
                        path: "/game/:alias/apply",
                        name: "game-apply",
                        component: () => import("@/views/games/game/Application.vue"),
                        props: true,
                        meta: {
                            middleware: [loadUser]
                        }
                    },
                    {
                        path: "/game/:alias/application/:userId",
                        name: "game-application",
                        component: () => import("@/views/games/game/Application.vue"),
                        props: true,
                        meta: {
                            // middleware: [loadUser]
                        }
                    },
                    {
                        path: "/game/:alias/players",
                        name: "game-players",
                        component: () => import("@/views/games/game/Players.vue"),
                        props: true,
                        meta: {
                            // middleware: [loadUser]
                        }
                    },
                ]
            },
        ],
    },
    {
        path: "/sign",
        redirect: "/sign-in",
        component: () => import("@/views/auth/Auth.vue"),
        children:
            [
                {
                    path: "/sign-in",
                    name: "sign-in",
                    component: () => import("@/views/auth/SignIn.vue"),
                    meta: {
                        middleware: [guest]
                    }
                },
                {
                    path: "/sign-up",
                    name: "sign-up",
                    component: () => import("@/views/auth/SignUp.vue"),
                    meta: {
                        middleware: [guest]
                    }
                },
                {
                    path: "/lost-pass",
                    name: "lost-pass",
                    component: () => import("@/views/auth/LostPass.vue"),
                    meta: {
                        middleware: [guest]
                    }
                },
                {
                    path: "/sign-out",
                    name: "sign-out",
                    component: () => import("@/views/auth/SignOut.vue"),
                    meta: {
                        middleware: [isAuth]
                    }
                },
                {
                    path: "/reset-pass/:uid/:token",
                    name: "reset-pass",
                    component: () => import("@/views/auth/PasswordReset.vue"),
                    props: true,
                    meta: {
                        middleware: []
                    }
                }
            ]
    },
    {
        // the 404 route, when none of the above matches
        path: "/404",
        name:
            "404",
        component:
            () => import("@/views/error/Error404.vue")
    },
    {
        path: "/:pathMatch(.*)*",
        redirect:
            "/404"
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

function middlewarePipeline(context, middleware, index, next) {
    const nextMiddleware = middleware[index]
    if (!nextMiddleware) {
        return context.next
    }
    return data => {
        if (data !== undefined) return next(data)
        const nextPipeline = middlewarePipeline(
            context,
            middleware,
            index + 1,
            next
        )
        return nextMiddleware({...context, next: nextPipeline})
    }
}

router.beforeEach((to, from, next) => {
    setPageTitle("Какие-то люди")
    store.commit("config/" + Mutations.RESET_LAYOUT_CONFIG)
    setTimeout(() => {
        window.scrollTo(0, 0)
    }, 100)

    const middleware = to.meta?.middleware
    // updateSubscriptionInfo({next: () => undefined})

    // if (middleware == undefined) {
    //   return next();
    // }

    const context = {
        to,
        from,
        next
    }
    /* @ts-ignore */
    return (
        (middleware &&
            middleware[0] &&
            middleware[0]({
                ...context,
                next: middlewarePipeline(context, middleware, 1, next)
            })) ||
        next()
    )
})

export default router
