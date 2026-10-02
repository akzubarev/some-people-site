import { redirect, type LoaderFunctionArgs } from 'react-router'
import { api, session } from '../../shared/api/client'
import type { components } from '../../shared/api/schema'

export type OrganizerGame = components['schemas']['OrganizerGame']
export type OrganizerIndex = components['schemas']['OrganizerGameIndex']
export type GameWrite = components['schemas']['OrganizerGameRequest']

export async function organizerLoader({ request, params }: LoaderFunctionArgs) {
  const { user } = await session(request.signal)
  if (!user) throw redirect('/sign-in?next=' + encodeURIComponent(new URL(request.url).pathname))
  if (!user.mg) throw new Response(null, { status: 403 })
  const index = await api<OrganizerIndex>('organizer/games/', { signal: request.signal })
  const game = params.game_id ? index.games.find(item => String(item.id) === params.game_id) : undefined
  if (params.game_id && !game) throw new Response(null, { status: 404 })
  const creating = new URL(request.url).pathname.endsWith('/new')
  if (creating && !index.permissions.add) throw new Response(null, { status: 403 })
  return { ...index, game, creating }
}

/** The API accepts local date/time in its configured time zone, shown beside the inputs. */
export function gameDateInput(value: string | null | undefined, timezone: string) {
  if (!value) return ''
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: timezone, year: 'numeric', month: '2-digit',
    day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' })
    .formatToParts(new Date(value))
  const part = (key: string) => parts.find(item => item.type === key)!.value
  return `${part('year')}-${part('month')}-${part('day')}T${part('hour')}:${part('minute')}:${part('second')}`
}
