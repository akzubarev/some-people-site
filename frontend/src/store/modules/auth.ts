import authService from "@/services/authService"
import {Actions, Mutations} from "@/store/enums/StoreEnums"
import {Module, Action, Mutation, VuexModule} from "vuex-module-decorators"
import Cookies from "js-cookie"

// export interface User {
//   name: string;
//   surname: string;
//   email: string;
// }

@Module
export default class AuthModule extends VuexModule {
    userObj = {}
    authToken = Cookies.get("auth_token")

    /**
     * Get current user object
     * @returns User
     */
    // get currentUser(): User {
    //   return this.user;
    // }

    /**
     * Verify user authentication
     * @returns boolean
     */

    get user(): object {
        return this.userObj
    }

    get token(): string {
        /* @ts-ignore */
        return this.authToken != "undefined" && this.authToken
    }

    get active(): boolean {
        return !(!this.authToken || this.authToken == "null")
    }

    @Mutation
    [Mutations.SET_USER](user) {
        this.userObj = user
    }

    @Mutation
    [Mutations.SET_TOKEN](token) {
        this.authToken = token
        Cookies.set("auth_token", token, {expires: 365})
    }

    @Action
    [Actions.SET_TOKEN](token) {
        this.context.commit(Mutations.SET_TOKEN, token)
    }

    @Action
    [Actions.SET_USER](user) {
        this.context.commit(Mutations.SET_USER, user)
    }

    @Action
    [Actions.LOGOUT]() {
        this.context.commit(Mutations.SET_USER, {})
        // Cookies.remove("auth_token")
        Cookies.remove("sessionid")
        Cookies.remove("csrftoken")
        this.context.commit(Mutations.SET_TOKEN, undefined)
    }
}
