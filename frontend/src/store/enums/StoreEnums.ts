enum Actions {
  // action types
  ADD_BODY_CLASSNAME = "addBodyClassName",
  HIDE_ACTION_LOADER = "hideActionLoader",
  SHOW_ACTION_LOADER = "showActionLoader",
  REMOVE_BODY_CLASSNAME = "removeBodyClassName",
  ADD_BODY_ATTRIBUTE = "addBodyAttribute",
  REMOVE_BODY_ATTRIBUTE = "removeBodyAttribute",
  ADD_CLASSNAME = "addClassName",
  SET_TOKEN = "setToken",
  SET_USER = "setUser",
  LOGOUT = "logout",
  SET_BREADCRUMB_ACTION = "setBreadcrumbAction",

  SET_GAMES = "setGames",
  SET_GROUPS = "setGroups",
  SET_APPLICATION = "setApplication",
  SET_QUESTIONS = "setQuestions",
}

enum Mutations {
  // mutation types
  SET_CLASSNAME_BY_POSITION = "appendBreadcrumb",
  SET_TOKEN = "SET_TOKEN",
  SET_USER = "SET_USER",
  SET_BREADCRUMB_MUTATION = "setBreadcrumbMutation",
  SET_LAYOUT_CONFIG = "setLayoutConfig",
  RESET_LAYOUT_CONFIG = "resetLayoutConfig",
  OVERRIDE_LAYOUT_CONFIG = "overrideLayoutConfig",
  OVERRIDE_PAGE_LAYOUT_CONFIG = "overridePageLayoutConfig",
  SET_HIDE_ACTION_LOADER = "setHideActionLoader",
  SET_SHOW_ACTION_LOADER = "setShowActionLoader",

  SET_GAMES = "SET_GAMES",
  SET_GROUPS = "SET_GROUPS",
  SET_APPLICATION = "SET_APPLICATION",
  SET_QUESTIONS = "SET_QUESTIONS",
}

export { Actions, Mutations }
