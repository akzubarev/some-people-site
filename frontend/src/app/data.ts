import { redirect, type LoaderFunctionArgs, type ActionFunctionArgs } from 'react-router'
import { api, ApiError, authenticate, json, query, safeNext, session } from '../shared/api/client'
import type { Application, Game, Group, Character, PublicPlayer, Question, Tag } from '../shared/api/types'

export async function rootLoader({ request }: LoaderFunctionArgs) {
  const [auth, games] = await Promise.all([
    session(request.signal), api<Game[]>('games/', { signal: request.signal }),
  ])
  return { user: auth.user, games }
}

async function requireUser(request: Request) {
  const { user } = await session(request.signal)
  if (!user) {
    const url = new URL(request.url)
    throw redirect('/sign-in?next=' + encodeURIComponent(url.pathname + url.search))
  }
  return user
}

export async function gameLoader({ request, params }: LoaderFunctionArgs) {
  const alias = params.game_alias || 'whales'
  const game = await api<Game>('games/' + encodeURIComponent(alias) + '/', { signal: request.signal })
  return { game }
}

export async function rolesLoader({ request, params }: LoaderFunctionArgs) {
  const alias = params.game_alias!
  return api<Group[]>(query('games/groups/', { game_alias: alias }), { signal: request.signal })
}

export async function charactersLoader({ request, params }: LoaderFunctionArgs) {
  const search = new URL(request.url).searchParams
  const [characters, tags] = await Promise.all([
    api<Character[]>(query('games/characters/', {
      game_alias: params.game_alias!, search: search.get('search'), tag: search.get('tag'),
    }), { signal: request.signal }),
    api<Tag[]>(query('games/tags/', { game_alias: params.game_alias! }), { signal: request.signal }),
  ])
  return { characters, tags }
}

export async function accountLoader({ request, params }: LoaderFunctionArgs) {
  await requireUser(request)
  const alias = params.game_alias!
  const [game, application, questions] = await Promise.all([
    api<Game>('games/' + encodeURIComponent(alias) + '/', { signal: request.signal }),
    api<Application | Record<string, never>>(query('applications/get/', { game_alias: alias }), { signal: request.signal }),
    api<Question[]>(query('questions/', { game_alias: alias }), { signal: request.signal }),
  ])
  return { game, application: 'id' in application ? application as Application : null, questions }
}

export async function settingsLoader({ request }: LoaderFunctionArgs) {
  return requireUser(request)
}
export async function mgLoader({ request }: LoaderFunctionArgs) {
  const user = await requireUser(request)
  if (!user.mg) throw new Response(null, { status: 403 })
  return api<PublicPlayer[]>('users/mg/', { signal: request.signal })
}

export type ActionResult = { error?: Record<string, unknown>; saved?: boolean; code?: string; url?: string; expires_in?: number }
async function actionResult(work: () => Promise<ActionResult | Response>): Promise<ActionResult | Response> {
  try { return await work() }
  catch (error) {
    if (error instanceof Response) throw error
    if (error instanceof ApiError) return { error: error.fields }
    return { error: { detail: 'Нет связи с сервером. Изменения не сохранены. Попробуйте снова.' } }
  }
}
export function authAction({ request }: ActionFunctionArgs) {
  return actionResult(async () => {
    const form = await request.formData()
    const path = new URL(request.url).pathname
    if (path === '/sign-out') await authenticate('session/', {}, 'DELETE')
    else {
      const payload = Object.fromEntries([...form].filter(([key]) => key !== 'next' && key !== 'password_confirm'))
      if (path === '/sign-up' && form.get('password') !== form.get('password_confirm'))
        return { error: { password: 'Пароли не совпадают.' } }
      await authenticate(path === '/sign-up' ? 'session/register/' : 'session/', payload)
    }
    return redirect(path === '/sign-out' ? '/' : safeNext(form.get('next')))
  })
}
export function settingsAction({ request }: ActionFunctionArgs) {
  return actionResult(async () => {
    await requireUser(request)
    const form = await request.formData()
    if (form.get('intent') === 'telegram')
      return json<ActionResult>('users/telegram_link/', {})
    form.delete('intent')
    for (const field of ['vk_public', 'tg_public']) form.set(field, form.has(field) ? 'true' : 'false')
    const avatar = form.get('avatar')
    if (!(avatar instanceof File) || !avatar.size) form.delete('avatar')
    await api('users/update_me/', { method: 'PUT', body: form })
    return { saved: true }
  })
}
export function applicationAction({ request, params }: ActionFunctionArgs) {
  return actionResult(async () => {
    await requireUser(request)
    const form = await request.formData()
    const intent = form.get('intent')
    const payload: Record<string, unknown> = { game_alias: params.game_alias }
    if (intent === 'save') {
      for (const [key, value] of form) {
        if (key.startsWith('question_') && typeof value === 'string') payload[key] = JSON.parse(value)
      }
    }
    const endpoint = intent === 'delete' ? 'delete' : intent === 'restore' ? 'restore' : 'apply'
    await json('applications/' + endpoint + '/', payload)
    return { saved: true }
  })
}
export function likeAction({ request, params }: ActionFunctionArgs) {
  return actionResult(async () => {
    await requireUser(request)
    const form = await request.formData()
    await json('users/like_character/', {
      game_alias: params.game_alias, character_id: Number(form.get('character_id')),
      like: form.get('like') === 'true',
    })
    return { saved: true }
  })
}
