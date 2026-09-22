import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { Actions, Mutations } from '@/store/enums/StoreEnums'

@Module
export default class BodyModule extends VuexModule {
  actionLoaderVisible = false
  get actionLoader(): boolean { return this.actionLoaderVisible }
  @Mutation
  [Mutations.SET_SHOW_ACTION_LOADER]() { this.actionLoaderVisible = true }
  @Mutation
  [Mutations.SET_HIDE_ACTION_LOADER]() { this.actionLoaderVisible = false }
  @Action
  [Actions.SHOW_ACTION_LOADER]() { this.context.commit(Mutations.SET_SHOW_ACTION_LOADER) }
  @Action
  [Actions.HIDE_ACTION_LOADER]() { this.context.commit(Mutations.SET_HIDE_ACTION_LOADER) }
}
