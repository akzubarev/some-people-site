enum Actions {
  // action types
  ADD_BODY_CLASSNAME = "addBodyClassName",
  HIDE_ACTION_LOADER = "hideActionLoader",
  SHOW_ACTION_LOADER = "showActionLoader",
  REMOVE_BODY_CLASSNAME = "removeBodyClassName",
  ADD_BODY_ATTRIBUTE = "addBodyAttribute",
  REMOVE_BODY_ATTRIBUTE = "removeBodyAttribute",
  ADD_CLASSNAME = "addClassName",
  ADD_EXPANDED_USER = "addExpandedUser",
  REMOVE_LAST_EXPANDED_USER = "removeLastExpandedUser",
  SET_TOKEN = "setToken",
  SET_USER = "setUser",
  LOGOUT = "logout",
  SET_BREADCRUMB_ACTION = "setBreadcrumbAction",

  GET_WALLET = "getWallet",
  GET_TRANSACTIONS = "getTransactions"
}

enum Mutations {
  // mutation types
  SET_CLASSNAME_BY_POSITION = "appendBreadcrumb",
  PURGE_AUTH = "logOut",
  SET_TOKEN = "SET_TOKEN",
  SET_USER = "SET_USER",
  ADD_EXPANDED_USER = "SET_EXPANDED_USER",
  REMOVE_LAST_EXPANDED_USER = "REMOVE_LAST_EXPANDED_USER",
  SET_PASSWORD = "setPassword",
  SET_ERROR = "setError",
  SET_BREADCRUMB_MUTATION = "setBreadcrumbMutation",
  SET_LAYOUT_CONFIG = "setLayoutConfig",
  RESET_LAYOUT_CONFIG = "resetLayoutConfig",
  OVERRIDE_LAYOUT_CONFIG = "overrideLayoutConfig",
  OVERRIDE_PAGE_LAYOUT_CONFIG = "overridePageLayoutConfig",
  SET_HIDE_ACTION_LOADER = "setHideActionLoader",
  SET_SHOW_ACTION_LOADER = "setShowActionLoader",

  SET_WALLET = "setWallet",
  SET_SUBSCRIPTIONS_COUNT = "setSubscripitonsCount",
  SET_TRANSACTIONS = "setTransactions"
}

export { Actions, Mutations }
