import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router"
import store from "@/store"
import {Mutations} from "@/store/enums/StoreEnums"
import {isAuth, isMg, guest} from "@/middleware/auth"
import {loadUser} from "@/middleware/load"
import {setPageTitle} from "@/store"
import Layout from "@/layout/Layout.vue"

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        component: Layout,
        children: [
            {
                path: "/",
                name: "main",
                component: () => import("@/views/title/Title.vue"),
                meta: {
                    middleware: [loadUser, guest]
                }
            },
            {
                path: "/mg",
                name: "mg",
                component: () => import("@/views/title/MG.vue"),
                meta: {
                    middleware: [loadUser, guest]
                }
            },
            {
                path: "/account/profile",
                name: "account-profile",
                component: () => import("@/views/account/Profile.vue"),
                meta: {
                    middleware: [loadUser, isAuth]
                }
            },
            {
                path: "/account/settings",
                name: "account-settings",
                component: () => import("@/views/account/settings/Settings.vue"),
                meta: {
                    middleware: [loadUser, isAuth]
                }
            },
            {
                path: "/games",
                name: "games",
                component: () => import("@/views/games/games/Games.vue"),
                meta: {
                    middleware: [loadUser, guest]
                }
            },
            {
                path: "/game/:game_alias",
                name: "game",
                redirect: "/game/:game_alias/about",
                component: () => import("@/views/games/GameRoot.vue"),
                props: true,
                children: [
                    {
                        path: "/game/:game_alias/about",
                        name: "game-about",
                        component: () => import("@/views/games/About.vue"),
                        props: true,
                        meta: {
                            middleware: [loadUser, guest]
                        }
                    },
                    {
                        path: "/game/:game_alias/roles",
                        name: "game-roles",
                        component: () => import("@/views/games/roles/Roles.vue"),
                        props: true,
                        meta: {
                            middleware: [loadUser, guest]
                        }
                    },
                    {
                        path: "/game/:game_alias/characters",
                        name: "game-characters",
                        component: () => import("@/views/games/roles/CharacterList.vue"),
                        props: true,
                        meta: {
                            middleware: [loadUser, guest]
                        }
                    },
                    {
                        path: "/game/:game_alias/apply",
                        name: "game-apply",
                        component: () => import("@/views/games/apply/Application.vue"),
                        props: true,
                        meta: {
                            middleware: [loadUser, isAuth]
                        }
                    },
                    {
                        path: "/game/:game_alias/application/:userId",
                        name: "game-application",
                        component: () => import("@/views/games/apply/Application.vue"),
                        props: true,
                        meta: {
                            middleware: [loadUser, isMg]
                        }
                    },
                    // {
                    //     path: "/game/:game_alias/players",
                    //     name: "game-players",
                    //     component: () => import("@/views/games/game/Players.vue"),
                    //     props: true,
                    //     meta: {
                    //         middleware: [loadUser, isMg]
                    //     }
                    // },
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
                        middleware: [loadUser, isAuth]
                    }
                },
                {
                    path: "/sign-out",
                    name: "sign-out",
                    component: () => import("@/views/auth/SignOut.vue"),
                    meta: {
                        middleware: [loadUser, isAuth]
                    }
                },
                {
                    path: "/reset-pass/:uid/:token",
                    name: "reset-pass",
                    component: () => import("@/views/auth/PasswordReset.vue"),
                    props: true,
                    meta: {
                        middleware: [loadUser, isAuth]
                    }
                }
            ]
    },
    {
        // the 404 route, when none of the above matches
        path: "/404",
        name: "404",
        component: () => import("@/views/error/Error404.vue")
    },
    {
        path: "/:pathMatch(.*)*",
        redirect: "/404"
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth',
            }
        }
    }
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
