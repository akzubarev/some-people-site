import {Actions, Mutations} from "@/store/enums/StoreEnums"
import {Module, Action, Mutation, VuexModule} from "vuex-module-decorators"


@Module
export default class GameModule extends VuexModule {
    gamesObj = {}
    groupsObj = []
    applicationObj = {}
    questionsObj = []

    get games(): object {
        return this.gamesObj
    }

    get groups(): object {
        return this.groupsObj
    }

    get application(): object {
        return this.applicationObj
    }

    get questions(): object {
        return this.questionsObj
    }

    get answers(): object {
        return this.applicationObj['answers'] || {'unfilled': [], 'values': {}}
    }

    get questionnaire_unfilled(): Number {
        return this.questionsObj ? this.questionsObj.filter(
            q => q['order'] > 0 && q['order'] && this.answers['unfilled'].includes(q['id'])
        ).length : 0
    }

    get application_unfilled(): Number {
        return this.questionsObj ? this.questionsObj.filter(
            q => q['order'] < 0 && q['order'] && this.answers['unfilled'].includes(q['id'])
        ).length : 0
    }

    @Mutation
    [Mutations.SET_GAMES](games) {
        this.gamesObj = games
    }

    @Mutation
    [Mutations.SET_GROUPS](groups) {
        this.groupsObj = groups
    }

    @Mutation
    [Mutations.SET_APPLICATION](application) {
        this.applicationObj = application
    }

    @Mutation
    [Mutations.SET_QUESTIONS](questions) {
        this.questionsObj = questions
    }

    @Action
    [Actions.SET_GAMES](games) {
        this.context.commit(Mutations.SET_GAMES, games)
    }

    @Action
    [Actions.SET_APPLICATION](application) {
        this.context.commit(Mutations.SET_APPLICATION, application)
    }

    @Action
    [Actions.SET_QUESTIONS](questions) {
        this.context.commit(Mutations.SET_QUESTIONS, questions)
    }

    @Action
    [Actions.SET_GROUPS](groups) {
        this.context.commit(Mutations.SET_GROUPS, groups)
    }
}
