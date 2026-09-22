enum Actions {
  // action types
  HIDE_ACTION_LOADER = "hideActionLoader",
  SHOW_ACTION_LOADER = "showActionLoader",
  SET_TOKEN = "setToken",
  SET_USER = "setUser",
  LOGOUT = "logout",

  SET_GAMES = "setGames",
  SET_GROUPS = "setGroups",
  SET_APPLICATION = "setApplication",
  SET_QUESTIONS = "setQuestions",
}

enum Mutations {
  // mutation types
  SET_TOKEN = "SET_TOKEN",
  SET_USER = "SET_USER",
  SET_HIDE_ACTION_LOADER = "setHideActionLoader",
  SET_SHOW_ACTION_LOADER = "setShowActionLoader",

  SET_GAMES = "SET_GAMES",
  SET_GROUPS = "SET_GROUPS",
  SET_APPLICATION = "SET_APPLICATION",
  SET_QUESTIONS = "SET_QUESTIONS",
}

export { Actions, Mutations }
