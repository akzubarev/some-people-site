import { createBrowserRouter, redirect, type LoaderFunctionArgs } from 'react-router'
import { Shell } from './Shell'
import { RouteError } from '../shared/ui'
import { PageLoading } from '../shared/Loading'
import { rootLoader, gameLoader, rolesLoader, charactersLoader, accountLoader, settingsLoader,
  mgLoader, authAction, settingsAction, applicationAction, likeAction } from './data'

export const router = createBrowserRouter([{
  id: 'root', Component: Shell, loader: rootLoader, ErrorBoundary: RouteError,
  HydrateFallback: PageLoading,
  children: [
    { index: true, loader: gameLoader, lazy: () => import('../features/games/About') },
    { path: 'game/:game_alias', loader: ({ params }: LoaderFunctionArgs) => redirect('/game/' + params.game_alias + '/about') },
    { path: 'game/:game_alias/about', loader: gameLoader, lazy: () => import('../features/games/About') },
    { path: 'game/:game_alias/roles', loader: rolesLoader, action: likeAction, lazy: () => import('../features/games/Roles') },
    { path: 'game/:game_alias/characters', loader: charactersLoader, action: likeAction, lazy: () => import('../features/games/Characters') },
    { path: 'account', loader: () => redirect('/account/whales/application') },
    { path: 'account/:game_alias/application', loader: accountLoader, action: applicationAction, lazy: () => import('../features/account/Application') },
    { path: 'account/:game_alias/questionnaire', loader: accountLoader, action: applicationAction, lazy: () => import('../features/account/Questionnaire') },
    { path: 'account/settings', loader: settingsLoader, action: settingsAction, lazy: () => import('../features/account/Settings') },
    { path: 'mg', loader: mgLoader, lazy: () => import('../features/account/Masters') },
    ...['sign-in', 'sign-up', 'sign-out'].map(path => ({
      path, action: authAction, lazy: () => import('../features/auth/Auth'),
    })),
    { path: 'sign', loader: () => redirect('/sign-in') },
    { path: '*', loader: () => { throw new Response(null, { status: 404 }) }, ErrorBoundary: RouteError },
  ].map(route => ({ ErrorBoundary: RouteError, ...route })),
}])
