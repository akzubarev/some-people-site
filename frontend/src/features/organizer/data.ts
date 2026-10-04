import { redirect, type LoaderFunctionArgs } from 'react-router'
import { api, session } from '../../shared/api/client'
import type { components } from '../../shared/api/schema'

export type OrganizerGame = components['schemas']['OrganizerGame']
export type OrganizerIndex = components['schemas']['OrganizerGameIndex']
export type GameWrite = components['schemas']['OrganizerGameRequest']
export type ContentEntity = components['schemas']['OrganizerGroup'] | components['schemas']['OrganizerCharacter']
  | components['schemas']['OrganizerTag'] | components['schemas']['OrganizerQuestion']
  | components['schemas']['OrganizerApplication'] | components['schemas']['OrganizerMailing']
export type Resource = 'groups' | 'characters' | 'tags' | 'questions' | 'applications' | 'mailings'
export const resources: Resource[] = ['groups', 'characters', 'tags', 'questions', 'applications', 'mailings']
export const sectionNames = { overview: 'Обзор игры', groups: 'Сетка и группы', characters: 'Персонажи',
  tags: 'Теги', questions: 'Опросник', applications: 'Заявки', contributions: 'Взносы', mailings: 'Рассылки' }

export async function organizerLoader({ request, params }: LoaderFunctionArgs) {
  const { user } = await session(request.signal)
  if (!user) throw redirect('/sign-in?next=' + encodeURIComponent(new URL(request.url).pathname))
  if (!user.mg) throw new Response(null, { status: 403 })
  const index = await api<OrganizerIndex>('organizer/games/', { signal: request.signal })
  const game = params.game_id ? index.games.find(item => String(item.id) === params.game_id) : undefined
  if (params.game_id && !game) throw new Response(null, { status: 404 })
  const creating = !params.section && new URL(request.url).pathname.endsWith('/new')
  if (creating && !index.permissions.add) throw new Response(null, { status: 403 })
  const section = params.section
  if (section && !(section in sectionNames)) throw new Response(null, { status: 404 })
  const context = game ? await api<components['schemas']['OrganizerContext']>(`organizer/games/${game.id}/context/`, { signal: request.signal }) : undefined
  const content: Partial<Record<Resource, ContentEntity[]>> = {}
  if (section && game && context) {
    const dependencies: Record<string, Resource[]> = {
      overview: resources, groups: ['groups'], characters: ['characters', 'groups', 'tags'], tags: ['tags'],
      questions: ['questions'], applications: ['applications', 'characters', 'questions'],
      contributions: ['applications', 'characters', 'questions'], mailings: ['mailings', 'applications'],
    }
    await Promise.all(dependencies[section].map(async resource => {
      const rights = context.permissions[resource]
      if (rights?.view || rights?.change) content[resource] = await api<ContentEntity[]>(`organizer/games/${game.id}/${resource}/`, { signal: request.signal })
    }))
  }
  const resource = section === 'contributions' ? 'applications' : section as Resource | undefined
  const recordId = params.record_id || (resource && content[resource]?.[0]?.id)
  if (params.record_id === 'new' && !context?.permissions[resource!]?.add) throw new Response(null, { status: 403 })
  const selected = recordId && recordId !== 'new' && game && resource
    ? await api<ContentEntity>(`organizer/games/${game.id}/${resource}/${recordId}/`, { signal: request.signal }) : undefined
  return { ...index, game, creating, section, context, content, selected, creatingRecord: params.record_id === 'new' }
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
