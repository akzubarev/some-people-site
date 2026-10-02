import { useEffect, useRef, useState, type ReactNode } from 'react'
import { Link, NavLink, useBeforeUnload, useBlocker, useLoaderData, useNavigate, useRevalidator } from 'react-router'
import { ApiError, api, json } from '../../shared/api/client'
import { gameImages } from '../../shared/assets'
import { Errors } from '../../shared/ui'
import { gameDateInput, type GameWrite, type OrganizerGame, type organizerLoader } from './data'
import './organizer.css'

const textFields = ['title', 'alias', 'short_description', 'description', 'location', 'vk', 'tg'] as const
const numberFields = ['price', 'player_count', 'year'] as const
const dateFields = ['start', 'end'] as const
const labels: Record<string, string> = { title: 'Название', alias: 'Алиас в адресе страницы',
  short_description: 'Короткое описание', description: 'Полное описание', location: 'Место',
  year: 'Год', start: 'Начало', end: 'Конец', player_count: 'Количество игроков', price: 'Взнос для новых заявок, ₽',
  vk: 'VK', tg: 'Telegram', expected_revision: 'Версия данных' }

function values(game: OrganizerGame | undefined, timezone: string) {
  return Object.fromEntries([
    ...textFields.map(key => [key, game?.[key] ?? '']),
    ...numberFields.map(key => [key, game?.[key]?.toString() ?? '']),
    ...dateFields.map(key => [key, gameDateInput(game?.[key], timezone)]),
  ]) as Record<string, string>
}

function Confirm({ title, children, accept, cancel, busy = false }: {
  title: string; children: ReactNode; accept: () => void; cancel: () => void; busy?: boolean
}) {
  const ref = useRef<HTMLDialogElement>(null)
  useEffect(() => { const dialog = ref.current!; dialog.showModal(); return () => dialog.close() }, [])
  return <dialog ref={ref} className="organizer-dialog" aria-label={title} onCancel={event => { event.preventDefault(); if (!busy) cancel() }}>
    <h2>{title}</h2>{children}<div className="organizer-actions">
      <button disabled={busy} onClick={cancel}>Остаться</button>
      <button disabled={busy} onClick={accept}>Продолжить без сохранения</button>
    </div></dialog>
}

export function Component() {
  const data = useLoaderData<typeof organizerLoader>()
  const navigate = useNavigate()
  const [menu, setMenu] = useState(false)
  return <div className="organizer-page" style={{ backgroundImage: `linear-gradient(#e0e5e4a8, #e0e5e4 550px), url(${gameImages(data.game?.alias || '').header})` }}>
    <div className="organizer-layout">
      <button className="organizer-menu-toggle" aria-expanded={menu} onClick={() => setMenu(!menu)}>Разделы кабинета</button>
      <aside className={'organizer-sidebar' + (menu ? ' is-open' : '')}>
        <label>Игра<select aria-label="Выбрать игру" value={data.game?.id ?? ''} onChange={event => {
          if (event.target.value) void navigate('/organizer/' + event.target.value)
        }}><option value="">Выберите игру</option>{data.games.map(game => <option value={game.id} key={game.id}>{game.title}</option>)}</select></label>
        <nav aria-label="Кабинет организатора">
          <NavLink end to="/organizer">Все игры</NavLink>
          {data.game && <NavLink to={'/organizer/' + data.game.id}>Настройки игры</NavLink>}
          {data.permissions.add && <NavLink to="/organizer/new">Создать игру</NavLink>}
          <Link to="/mg">Мастерская группа</Link>
        </nav>
        {data.game && <Link to={'/game/' + encodeURIComponent(data.game.alias) + '/about'}>Посмотреть страницу игры ↗</Link>}
      </aside>
      <main className="organizer-content"><div className="organizer-eyebrow">Кабинет организатора</div>
        {data.game || data.creating
          ? <GameEditor key={data.game?.id ?? 'new'} game={data.game} timezone={data.timezone}
            canEdit={data.game ? data.permissions.change : data.permissions.add} />
          : <><h1>Игры</h1><p>Выберите игру, чтобы изменить её содержание и публикацию.</p>
            <div className="organizer-game-list">{data.games.map(game => <Link to={'/organizer/' + game.id} key={game.id}>
              <h2>{game.title}</h2><p>{game.location || 'Место пока не указано'}</p>
              <span>{game.open_applications ? 'Приём заявок открыт' : 'Приём заявок закрыт'}</span>
            </Link>)}</div>
            {!data.games.length && <p>Пока нет игр.{data.permissions.add && <> <Link to="/organizer/new">Создать первую игру</Link></>}</p>}
          </>}
      </main>
    </div>
  </div>
}

function GameEditor({ game, timezone, canEdit }: { game?: OrganizerGame; timezone: string; canEdit: boolean }) {
  const navigate = useNavigate(), revalidator = useRevalidator()
  const [baseline, setBaseline] = useState(game)
  const [draft, setDraft] = useState(() => values(game, timezone))
  const [publication, setPublication] = useState({ open_applications: game?.open_applications ?? false,
    open_character_list: game?.open_character_list ?? false })
  const [saving, setSaving] = useState(false), [saved, setSaved] = useState(false), [reload, setReload] = useState(false)
  const [error, setError] = useState<Record<string, unknown>>()
  const [conflict, setConflict] = useState(false)
  const allowNavigation = useRef(false)
  const dirty = JSON.stringify(draft) !== JSON.stringify(values(baseline, timezone))
    || publication.open_applications !== (baseline?.open_applications ?? false)
    || publication.open_character_list !== (baseline?.open_character_list ?? false)
  const blocker = useBlocker(() => !allowNavigation.current && (dirty || saving))
  useBeforeUnload(event => { if (dirty || saving) { event.preventDefault(); event.returnValue = '' } })
  const externalChange = game && baseline && game.revision !== baseline.revision

  function reset(next: OrganizerGame | undefined) {
    setBaseline(next); setDraft(values(next, timezone)); setPublication({ open_applications: next?.open_applications ?? false,
      open_character_list: next?.open_character_list ?? false }); setConflict(false); setError(undefined); setSaved(false)
  }
  async function refresh() {
    if (!game) { reset(undefined); setReload(false); return }
    setSaving(true)
    try { reset(await api<OrganizerGame>(`organizer/games/${game.id}/`)); setReload(false) }
    catch { setError({ detail: 'Не удалось загрузить актуальные данные. Ваши изменения сохранены в форме.' }); setReload(false) }
    finally { setSaving(false) }
  }
  const input = (key: string, type = 'text', required = false) => <label key={key}>{labels[key]}
    <input name={key} type={type} required={required} value={draft[key]} maxLength={key === 'alias' ? 20 : type === 'text' ? 100 : undefined}
      min={['price', 'player_count'].includes(key) ? 0 : undefined} step={type === 'number' || type === 'datetime-local' ? 1 : undefined}
      pattern={key === 'alias' ? '[a-z][a-z0-9-]*' : undefined}
      onChange={event => { setDraft({ ...draft, [key]: event.target.value }); setSaved(false) }} />
  </label>
  const text = (key: string) => <label className="organizer-full">{labels[key]}<textarea name={key} value={draft[key]}
    onChange={event => { setDraft({ ...draft, [key]: event.target.value }); setSaved(false) }} /></label>
  async function save() {
    const payload: GameWrite = { title: draft.title.trim(), alias: draft.alias.trim(), ...publication }
    for (const key of textFields) if (key !== 'title' && key !== 'alias') payload[key] = draft[key] || null
    for (const key of numberFields) payload[key] = draft[key] === '' ? null : Number(draft[key])
    for (const key of dateFields) payload[key] = draft[key] === gameDateInput(baseline?.[key], timezone)
      ? baseline?.[key] ?? null : draft[key] || null
    if (baseline) payload.expected_revision = baseline.revision
    setSaving(true); setError(undefined); setSaved(false)
    try {
      const next = await json<OrganizerGame>('organizer/games/' + (baseline ? baseline.id + '/' : ''), payload, baseline ? 'PATCH' : 'POST')
      reset(next); setSaved(true)
      if (!baseline) { allowNavigation.current = true; void navigate('/organizer/' + next.id) }
      else void revalidator.revalidate()
    } catch (failure) {
      setError(failure instanceof ApiError ? failure.fields : { detail: 'Нет связи с сервером. Изменения остались в форме. Повторите сохранение.' })
      setConflict(failure instanceof ApiError && failure.status === 409)
    } finally { setSaving(false) }
  }
  return <>
    <h1>{game ? game.title : 'Создать игру'}</h1><p>Информация об игре и доступ для игроков.</p>
    {!canEdit && <p role="status">Доступен только просмотр. Для сохранения требуется право изменения игр.</p>}
    <form className="organizer-editor" onSubmit={event => { event.preventDefault(); void save() }}>
      <fieldset disabled={!canEdit || saving}><legend>Название и описание</legend><div className="organizer-fields">
        {input('title', 'text', true)}{input('alias', 'text', true)}{text('short_description')}{text('description')}
      </div><p className="organizer-note">Алиас задаёт адрес страницы. Его изменение сделает прежние ссылки недействительными.</p></fieldset>
      <fieldset disabled={!canEdit || saving}><legend>Когда, где и для кого</legend><div className="organizer-fields">
        {input('location')}{input('year', 'number')}{input('start', 'datetime-local')}{input('end', 'datetime-local')}
        {input('player_count', 'number')}{input('price', 'number')}
      </div><p className="organizer-note">Время игры: {timezone}. Новый взнос применяется к новым заявкам; существующие суммы сохраняются.</p></fieldset>
      <fieldset disabled={!canEdit || saving}><legend>Ссылки и публикация</legend><div className="organizer-fields">
        {input('vk')}{input('tg')}
        {(['open_applications', 'open_character_list'] as const).map(key => <label className="organizer-check" key={key}>
          <input type="checkbox" name={key} checked={publication[key]} disabled={!baseline}
            onChange={event => { setPublication({ ...publication, [key]: event.target.checked }); setSaved(false) }} />
          {key === 'open_applications' ? 'Принимать новые заявки' : 'Показывать сетку ролей'}</label>)}
      </div>{!baseline && <p className="organizer-note">Новая игра создаётся с закрытыми заявками и сеткой. Их можно открыть после сохранения.</p>}</fieldset>
      <Errors error={error && Object.fromEntries(Object.entries(error).map(([key, value]) => [key,
        labels[key] ? labels[key] + ': ' + (Array.isArray(value) ? value.join(' ') : String(value)) : value]))} />
      {(conflict || externalChange) && <p role="status">На сервере есть другая версия игры. Ваш текст остаётся в форме. Скопируйте нужные изменения перед загрузкой актуальных данных.</p>}
      <div className="organizer-actions">
        {canEdit && <button type="submit" disabled={saving || conflict}>{saving ? 'Сохраняем…' : baseline ? 'Сохранить игру' : 'Создать игру'}</button>}
        {(dirty || externalChange || conflict) && <button type="button" disabled={saving} onClick={() => setReload(true)}>Загрузить актуальные данные</button>}
      </div>
      <p role="status">{saved ? 'Игра сохранена.' : dirty ? 'Есть несохранённые изменения.' : ''}</p>
    </form>
    {reload && <Confirm title="Отказаться от изменений?" busy={saving} cancel={() => setReload(false)} accept={() => void refresh()}>
      <p>Введённые значения будут заменены актуальными данными.</p></Confirm>}
    {blocker.state === 'blocked' && <Confirm title="Есть несохранённые изменения" busy={saving}
      cancel={() => blocker.reset()} accept={() => blocker.proceed()}><p>Сохраните игру или подтвердите уход со страницы.</p></Confirm>}
  </>
}
