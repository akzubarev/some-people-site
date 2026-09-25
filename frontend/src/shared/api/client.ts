import type { Session } from './types'

export class ApiError extends Error {
  constructor(public status: number, public fields: Record<string, unknown>) {
    super(typeof fields.detail === 'string' ? fields.detail : 'Не удалось выполнить запрос.')
  }
}

let csrfToken: string | undefined

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const method = options.method || 'GET'
  const headers = new Headers(options.headers)
  headers.set('Accept', 'application/json')
  if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
    if (!csrfToken) await session(options.signal ?? undefined)
    headers.set('X-CSRFToken', csrfToken!)
  }
  const response = await fetch('/api/' + path, {
    ...options, headers, credentials: 'same-origin', cache: 'no-store',
  })
  const content = response.status === 204 ? null : await response.json().catch(() => null)
  if (!response.ok) throw new ApiError(response.status,
    content && typeof content === 'object' ? content : { detail: 'Сервер недоступен. Попробуйте ещё раз.' })
  return content as T
}

export async function session(signal?: AbortSignal): Promise<Session> {
  const result = await api<Session>('session/', { signal })
  csrfToken = result.csrfToken
  return result
}

export async function authenticate(path: string, payload: unknown, method = 'POST') {
  const result = await json<Session>(path, payload, method)
  csrfToken = result.csrfToken
  if (typeof BroadcastChannel !== 'undefined') {
    const channel = new BroadcastChannel('some-people-session')
    channel.postMessage('changed')
    channel.close()
  }
  return result
}

export function json<T>(path: string, payload: unknown, method = 'POST', signal?: AbortSignal) {
  return api<T>(path, { method, body: JSON.stringify(payload),
    headers: { 'Content-Type': 'application/json' }, signal })
}

export function query(path: string, params: Record<string, string | null>) {
  const search = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) if (value) search.set(key, value)
  return path + '?' + search.toString()
}

export function safeNext(value: FormDataEntryValue | string | null): string {
  return typeof value === 'string' && /^\/(?!\/)/.test(value) &&
    !value.includes('\\') && ![...value].some(character => character.charCodeAt(0) <= 32)
    ? value : '/account/'
}

export function publicLink(value: string | null, network?: 'vk' | 'tg') {
  if (!value) return undefined
  const candidate = /^https?:\/\//i.test(value) ? value
    : network && /^[\w.@-]+$/u.test(value) ? 'https://' + (network === 'vk' ? 'vk.com/' : 't.me/') + value.replace(/^@/, '') : ''
  try {
    const url = new URL(candidate)
    return ['http:', 'https:'].includes(url.protocol) && !url.username && !url.password ? url.href : undefined
  } catch { return undefined }
}
