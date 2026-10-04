import { lazy, Suspense, useEffect, useRef, useState, type ReactNode } from 'react'
import { Link, useBeforeUnload, useBlocker, useNavigate, useRevalidator } from 'react-router'
import { ApiError, api, json } from '../../shared/api/client'
import { Errors } from '../../shared/ui'
import type { components } from '../../shared/api/schema'
import type { organizerLoader, Resource, ContentEntity } from './data'
import { sectionNames, gameDateInput } from './data'
import { QuestionChoices } from './QuestionChoices'
const RichText = lazy(() => import('./RichText').then(module => ({ default: module.RichText })))

type Data = Awaited<ReturnType<typeof organizerLoader>>
type Values = Record<string, unknown>
const object = (value: unknown): Values => value && typeof value === 'object' && !Array.isArray(value) ? value as Values : {}
const text = (value: unknown) => value == null ? '' : String(value)
const list = (value: unknown): number[] => Array.isArray(value) ? value.filter((v): v is number => typeof v === 'number') : []
const name = (entity: unknown) => { const value = object(entity); return text(value.name || value.title || object(value.player).name || `Рассылка №${value.id}`) }
const statuses = { pending: 'Подана', discussing: 'Обсуждается', confirmed: 'Принята', declined: 'Отклонена', deleted: 'Удалена' }
const questionTypes = { line: 'Строка', paragraph: 'Абзац', single_choice: 'Одиночный выбор', multiple_choice: 'Множественный выбор', scale: 'Шкала', matrix: 'Сетка', matrix_checkbox: 'Сетка флажков' }

export function ContentWorkspace({ data }: { data: Data }) {
  const [search, setSearch] = useState(''), [status, setStatus] = useState('')
  const section = data.section as keyof typeof sectionNames
  const resource = (section === 'contributions' ? 'applications' : section) as Resource
  const records = data.content[resource] || []
  const ancestry = (row: ContentEntity) => { const names: string[] = []; const seen = new Set([row.id]); let parent = object(row).parent
    while (typeof parent === 'number' && !seen.has(parent)) { seen.add(parent); const item = records.find(item => item.id === parent); if (!item) break; names.unshift(name(item)); parent = object(item).parent }
    return names.join(' / ') }
  const rights = data.context?.permissions[resource] || {}
  const base = `/organizer/${data.game!.id}/${section}`
  const selected = data.selected || (!data.creatingRecord ? records[0] : undefined)
  if (section === 'overview') return <><h1>{data.game!.title}</h1><p>Все разделы используют одни и те же данные игры.</p>
    <div className="organizer-game-list">{Object.entries(data.content).filter(([key]) => key !== 'tags').map(([key, rows]) => <Link key={key} to={`/organizer/${data.game!.id}/${key}`}>
      <h2>{sectionNames[key as Resource]}</h2><strong>{rows.length}</strong></Link>)}</div>
    {data.content.applications && <div className="organizer-editor"><h2>Взносы и анкеты</h2><p>Получено: {data.content.applications.reduce((sum, app) => sum + Number(object(app).payed || 0), 0)} ₽</p>
      <p>Незаполненные анкеты: {data.content.applications.filter(app => list(object(app).missing_questions).length).length}</p></div>}</>
  return <><div className="organizer-section-heading"><div><h1>{sectionNames[section]}</h1><p>{data.game!.title}</p></div>
    {rights.add && resource !== 'applications' && <Link className="organizer-create" to={base + '/new'}>Создать {resource === 'questions' ? 'вопрос' : resource === 'characters' ? 'персонажа' : resource === 'mailings' ? 'рассылку' : resource === 'tags' ? 'тег' : 'группу'}</Link>}</div>
    {!(rights.view || rights.change || (data.creatingRecord && rights.add)) ? <p>Нет права просмотра этого раздела.</p> : <div className="organizer-content-layout">
      <aside className="organizer-record-list"><label>Поиск<input value={search} onChange={e => setSearch(e.target.value)} /></label>
        {resource === 'applications' && <label>Статус<select value={status} onChange={e => setStatus(e.target.value)}><option value="">Все статусы</option>{Object.entries(statuses).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>}
        {records.filter(row => name(row).toLocaleLowerCase().includes(search.toLocaleLowerCase()) && (!status || object(row).status === status)).map(row => <Link key={row.id}
          className={selected?.id === row.id && !data.creatingRecord ? 'active' : ''} to={base + '/' + row.id}>
          {Boolean(object(row).image) && <img src={text(object(row).image)} alt="" />}
          <span>{resource === 'groups' && ancestry(row) && <small>{ancestry(row)}</small>}<strong>{name(row)}</strong>{resource === 'groups' && <small>{object(row).family ? 'Семья' : 'Фракция'} · {object(row).hidden ? 'Скрыта' : 'Открыта'}</small>}
            {resource === 'applications' && <small>{statuses[text(object(row).status) as keyof typeof statuses]} · {text(object(row).payed)} / {text(object(row).price) || '0'} ₽</small>}
            {resource === 'mailings' && <small>{object(row).ready ? 'Подтверждена' : 'Черновик'}</small>}</span></Link>)}
        {!records.length && <p>Пока нет записей.</p>}</aside>
      {selected || data.creatingRecord ? <RecordEditor key={`${section}:${data.creatingRecord ? 'new' : selected!.id}`} data={data} resource={resource}
        initial={data.creatingRecord ? undefined : selected} /> : <p>Выберите запись или создайте новую.</p>}
    </div>}</>
}

function Modal({ title, children, close }: { title: string; children: ReactNode; close: () => void }) {
  const ref = useRef<HTMLDialogElement>(null)
  useEffect(() => { const dialog = ref.current!; dialog.showModal(); return () => dialog.close() }, [])
  return <dialog ref={ref} className="organizer-dialog" aria-label={title} onCancel={e => { e.preventDefault(); close() }}><h2>{title}</h2>{children}</dialog>
}

function RecordEditor({ data, resource, initial }: { data: Data; resource: Resource; initial?: ContentEntity }) {
  const navigate = useNavigate(), revalidator = useRevalidator()
  const defaults: Values = { name: '', title: '', alias: '', order: 1, hidden: false, family: resource === 'groups' ? false : null,
    group: null, master: null, tags: [], required: true, type: 'line', choices: null, games: [data.game!.id],
    color: '#99c6b2', private: false, mg: false, text: '', applications: [], time: '', description: '' }
  const [baseline, setBaseline] = useState(initial), [draft, setDraft] = useState<Values>(() => initial ? { ...initial } : defaults)
  const [files, setFiles] = useState<Record<string, File>>({}), [busy, setBusy] = useState(false), [saved, setSaved] = useState(false)
  const [error, setError] = useState<Record<string, unknown>>(), [confirm, setConfirm] = useState<'delete' | 'hide' | 'mail' | 'reload'>()
  const [preview, setPreview] = useState<components['schemas']['MailingPreview']>()
  const [key] = useState(() => crypto.randomUUID())
  const [reason, setReason] = useState('')
  const dirty = JSON.stringify(draft) !== JSON.stringify(baseline || defaults) || Object.keys(files).length > 0
  const allowNavigation = useRef(false)
  const blocker = useBlocker(() => !allowNavigation.current && (dirty || busy))
  useBeforeUnload(e => { if (dirty || busy) { e.preventDefault(); e.returnValue = '' } })
  const rights = data.context?.permissions[resource] || {}
  const editable = Boolean(baseline ? rights.change : rights.add) && !draft.ready
  const endpoint = `organizer/games/${data.game!.id}/${resource}/`
  const set = (field: string, value: unknown) => { setDraft(current => ({ ...current, [field]: value })); setSaved(false); setPreview(undefined) }
  const field = (key: string, label: string, type = 'text', required = false) => <label key={key}>{label}<input type={type} required={required}
    value={text(draft[key])} min={type === 'number' && ['price', 'payed'].includes(key) ? 0 : undefined}
    onChange={e => set(key, type === 'number' ? e.target.value === '' ? null : Number(e.target.value) : e.target.value)} /></label>
  const area = (key: string, label: string) => <label className="organizer-full">{label}<textarea aria-label={label} value={text(draft[key])} onChange={e => set(key, e.target.value)} /></label>
  const check = (key: string, label: string) => <label className="organizer-check"><input type="checkbox" checked={Boolean(draft[key])} onChange={e => set(key, e.target.checked)} />{label}</label>
  const select = (key: string, label: string, options: { id: number; name: string }[]) => <label>{label}<select value={text(draft[key])} onChange={e => set(key, e.target.value ? Number(e.target.value) : null)}>
    <option value="">Не выбрано</option>{options.map(option => <option key={option.id} value={option.id}>{option.name}</option>)}</select></label>
  const groups = (data.content.groups || []).map(row => ({ id: row.id, name: name(row), family: Boolean(object(row).family), parent: object(row).parent }))
  const upload = (key: string, label: string, accept: string) => <div><label>{label}<input type="file" accept={accept} onChange={e => { const file = e.target.files?.[0]; if (file) { setFiles(current => ({ ...current, [key]: file })); setSaved(false) } }} /></label>
    {key === 'image' && Boolean(draft[key]) && <img className="organizer-portrait" src={text(draft[key])} alt="Текущее изображение" />}
    {key === 'kventa' && Boolean(draft[key]) && <a href={text(draft[key])} target="_blank" rel="noreferrer">Открыть PDF</a>}
    {Boolean(draft[key] || files[key]) && <button type="button" onClick={() => { set(key, null); setFiles(current => Object.fromEntries(Object.entries(current).filter(([k]) => k !== key))) }}>Удалить файл</button>}</div>
  const options = (key: string, title: string, rows: { id: number; label: string }[]) => <fieldset className="organizer-full organizer-options"><legend>{title}</legend>{rows.map(row => <label key={row.id} className="organizer-check">
    <input type="checkbox" checked={list(draft[key]).includes(row.id)} onChange={e => set(key, e.target.checked ? [...list(draft[key]), row.id] : list(draft[key]).filter(id => id !== row.id))} />{row.label}</label>)}</fieldset>
  const fields: Record<Resource, string[]> = {
    groups: ['name', 'alias', 'description', 'order', 'parent', 'family', 'hidden'],
    characters: ['name', 'name_eng', 'alias', 'description', 'order', 'group', 'family', 'master', 'tags'],
    tags: ['name', 'color', 'private', 'mg'], questions: ['title', 'description', 'type', 'choices', 'required', 'order', 'games'],
    applications: ['status', 'character', 'price', 'payed'], mailings: ['text', 'time', 'applications'],
  }
  function failure(error: unknown) { setError(error instanceof ApiError ? error.fields : { detail: 'Не удалось сохранить. Изменения остались в форме.' }) }
  async function save() {
    setBusy(true); setError(undefined); setConfirm(undefined)
    const payload: Values = Object.fromEntries(fields[resource].map(key => [key, draft[key] ?? (['alias', 'name_eng', 'description'].includes(key) ? '' : null)]))
    if (baseline) payload.expected_revision = baseline.revision
    payload.acknowledge_shared = Boolean(draft.acknowledge_shared)
    if (resource === 'applications') payload.reason = reason
    for (const key of ['image', 'kventa']) if (draft[key] === null && object(baseline)[key]) payload[key] = null
    try {
      const form = new FormData(); form.set('payload', JSON.stringify(payload)); Object.entries(files).forEach(([key, file]) => form.set(key, file))
      const next = await api<ContentEntity>(endpoint + (baseline ? baseline.id + '/' : ''), { method: baseline ? 'PATCH' : 'POST', body: form })
      setBaseline(next); setDraft({ ...next }); setFiles({}); setSaved(true); setReason('')
      if (!baseline) { allowNavigation.current = true; void navigate(`/organizer/${data.game!.id}/${data.section}/${next.id}`) }
      else void revalidator.revalidate()
    } catch (error) { failure(error) } finally { setBusy(false) }
  }
  async function remove() {
    setBusy(true)
    try { await json(endpoint + baseline!.id + '/', { expected_revision: baseline!.revision }, 'DELETE'); allowNavigation.current = true; void navigate(`/organizer/${data.game!.id}/${data.section}`) }
    catch (error) { failure(error) } finally { setBusy(false); setConfirm(undefined) }
  }
  async function refresh() {
    setBusy(true)
    try { const next = await api<ContentEntity>(endpoint + baseline!.id + '/'); setBaseline(next); setDraft({ ...next }); setFiles({}); setError(undefined); setReason('') }
    catch (error) { failure(error) } finally { setBusy(false); setConfirm(undefined) }
  }
  async function mailPreview() {
    setBusy(true); setError(undefined)
    try { setPreview(await api<components['schemas']['MailingPreview']>(endpoint + baseline!.id + '/preview/')); setConfirm('mail') }
    catch (error) { failure(error) } finally { setBusy(false) }
  }
  async function confirmMail() {
    setBusy(true)
    try { const next = await json<ContentEntity>(endpoint + baseline!.id + '/confirm/', { idempotency_key: key, audience_revision: preview!.audience_revision }); setBaseline(next); setDraft({ ...next }); setSaved(true); void revalidator.revalidate() }
    catch (error) { failure(error) } finally { setBusy(false); setConfirm(undefined) }
  }
  return <section className="organizer-record-editor"><h2>{baseline ? name(baseline) : 'Новая запись'}</h2>
    {!editable && <p>Доступен только просмотр.</p>}
    <form className="organizer-editor" onSubmit={e => { e.preventDefault(); if (resource === 'groups' && draft.hidden && !object(baseline).hidden) setConfirm('hide'); else void save() }}>
      <fieldset disabled={!editable || busy}><div className="organizer-fields">
        {(resource === 'groups' || resource === 'characters' || resource === 'tags') && field('name', 'Название', 'text', true)}
        {(resource === 'groups' || resource === 'characters') && <>{field('alias', 'Алиас', 'text', resource === 'characters')}{area('description', 'Описание')}{field('order', 'Порядок', 'number')}{upload('image', 'Изображение', 'image/*')}</>}
        {resource === 'groups' && <>{check('family', 'Это семья')}{check('hidden', 'Скрыть от игроков')}{select('parent', 'Родительская группа', groups.filter(row => row.id !== baseline?.id && row.family === Boolean(draft.family)))}
          <p className="organizer-note">Скрытие действует на дочерние группы и их персонажей. Дочерних групп: {list(object(baseline).descendants).length}. Связано персонажей: {text(object(baseline).character_count) || '0'}.</p></>}
        {resource === 'characters' && <>{field('name_eng', 'Имя на английском')}{select('group', 'Фракция', groups.filter(row => !row.family))}{select('family', 'Семья', groups.filter(row => row.family))}
          {select('master', 'Мастер', (data.context?.masters || []).map(row => ({ id: Number(row.id), name: text(row.name) })))}{upload('kventa', 'Текст персонажа (PDF)', 'application/pdf')}
          {options('tags', 'Теги', (data.content.tags || []).map(row => ({ id: row.id, label: name(row) })))}
          <p className="organizer-full"><Link to={`/organizer/${data.game!.id}/tags`}>Управление тегами</Link></p></>}
        {resource === 'tags' && <>{field('color', 'Цвет', 'color')}{check('private', 'Виден внутри тега')}{check('mg', 'Виден только МГ')}
          <p>Теги общие для игр. Используется в играх: {list(draft.used_games).map(id => data.games.find(game => game.id === id)?.title || id).join(', ') || 'пока нигде'}.</p>{check('acknowledge_shared', 'Подтверждаю изменение общего тега')}</>}
        {resource === 'questions' && <>{field('title', 'Вопрос', 'text', true)}{area('description', 'Описание и подсказка')}
          <label>Тип ответа<select disabled={Number(draft.answer_count) > 0} value={text(draft.type)} onChange={e => { set('type', e.target.value); set('choices', e.target.value.startsWith('matrix') ? [[], []] : []) }}>
            {Object.entries(questionTypes).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>{field('order', 'Порядок (отрицательный — при подаче заявки)', 'number')}{check('required', 'Обязательный ответ')}
          <QuestionChoices type={text(draft.type)} choices={draft.choices} title={text(draft.title)} disabled={!editable || busy || Number(draft.answer_count) > 0} change={value => set('choices', value)} />
          {options('games', 'Игры, использующие вопрос', data.games.map(game => ({ id: game.id, label: game.title })))}{check('acknowledge_shared', 'Подтверждаю изменение вопроса во всех выбранных играх')}
          <p>Сохранённых ответов: {text(draft.answer_count) || '0'}. Существующие ответы не удаляются при редактировании.</p></>}
        {resource === 'applications' && <>{data.section !== 'contributions' && <><label>Статус<select value={text(draft.status)} onChange={e => set('status', e.target.value)}>{Object.entries(statuses).map(([key, label]) => <option value={key} key={key}>{label}</option>)}</select></label>
          {select('character', 'Назначенный персонаж', (data.content.characters || []).map(row => ({ id: row.id, name: name(row) })))}</>}{field('price', 'Взнос, ₽', 'number')}{field('payed', 'Оплачено, ₽', 'number')}
          <label className="organizer-full">Причина изменения взноса<input value={reason} onChange={e => setReason(e.target.value)} maxLength={500} /></label></>}
        {resource === 'mailings' && <><div className="organizer-full"><Suspense fallback={<p>Загрузка редактора…</p>}><RichText uploadEndpoint={endpoint + 'upload/'} value={text(draft.text)} change={html => set('text', html)} disabled={!editable || busy} /></Suspense></div>
          <label>Время отправки ({data.timezone})<input type="datetime-local" step="1" required value={/Z$|[+-]\d{2}:\d{2}$/.test(text(draft.time)) ? gameDateInput(text(draft.time), data.timezone) : text(draft.time)} onChange={e => set('time', e.target.value)} /></label>
          <div className="organizer-full organizer-actions"><button type="button" onClick={() => set('applications', (data.content.applications || []).filter(row => list(object(row).missing_questions).length > 0).map(row => row.id))}>Не заполнили анкету</button>
            <button type="button" onClick={() => set('applications', (data.content.applications || []).filter(row => Number(object(row).payed) < Number(object(row).price)).map(row => row.id))}>Не доплатили взнос</button>
            <button type="button" onClick={() => set('applications', [])}>Снять выбор</button></div>
          {options('applications', 'Получатели — заявки этой игры', (data.content.applications || []).map(row => ({ id: row.id, label: name(row) + (object(object(row).player).telegram ? '' : ' · Telegram не привязан') })))}
          <p>Пустой выбор никому не отправляется. Сохранение создаёт только черновик.</p></>}
      </div></fieldset><Errors error={error} />
      <div className="organizer-actions">{editable && <button disabled={busy} type="submit">{busy ? 'Сохраняем…' : 'Сохранить'}</button>}
        {baseline && <button type="button" disabled={busy} onClick={() => setConfirm('reload')}>Загрузить актуальные данные</button>}
        {baseline && rights.delete && resource !== 'applications' && !draft.ready && <button type="button" disabled={busy} onClick={() => setConfirm('delete')}>Удалить запись</button>}
        {resource === 'mailings' && baseline && editable && <button type="button" disabled={busy || dirty} onClick={() => void mailPreview()}>Проверить получателей и подтвердить</button>}</div>
      <p role="status">{saved ? 'Сохранено.' : dirty ? 'Есть несохранённые изменения.' : ''}</p>
    </form>
    {resource === 'characters' && Boolean(draft.assigned_application) && <details><summary>Назначение игрока</summary><Link to={`/organizer/${data.game!.id}/applications/${draft.assigned_application}`}>Открыть связанную заявку</Link></details>}
    {resource === 'characters' && !draft.assigned_application && <details><summary>Назначение игрока</summary><Link to={`/organizer/${data.game!.id}/applications`}>Выбрать заявку для назначения</Link></details>}
    {resource === 'applications' && <p><Link to={`/organizer/${data.game!.id}/${data.section === 'contributions' ? 'applications' : 'contributions'}/${baseline!.id}`}>{data.section === 'contributions' ? 'Открыть заявку и назначение' : 'Открыть взносы'}</Link> · Осталось оплатить: {Math.max(0, Number(draft.price) - Number(draft.payed))} ₽</p>}
    {resource === 'applications' && <ApplicationDetails data={data} draft={draft} />}
    {resource === 'mailings' && Boolean(draft.ready) && <p>Запланировано: {text(object(draft.delivery).total)}, отправлено: {text(object(draft.delivery).sent)}, ошибок: {text(object(draft.delivery).failed)}.</p>}
    {resource === 'mailings' && Boolean(draft.ready) && Array.isArray(object(draft.delivery).recipients) && <ul>{(object(draft.delivery).recipients as Values[]).map(row => <li key={text(row.user_id)}>{name(data.content.applications?.find(app => object(object(app).player).id === row.user_id))}: {row.sent ? 'Отправлено' : row.last_error ? 'Ошибка: ' + text(row.last_error) : 'В очереди'} · попыток: {text(row.attempts)}</li>)}</ul>}
    {confirm && <Modal title={confirm === 'mail' ? 'Подтверждение рассылки' : confirm === 'hide' ? 'Скрыть группу и потомков?' : confirm === 'reload' ? 'Заменить изменения данными сервера?' : 'Удалить запись?'} close={() => !busy && setConfirm(undefined)}>
      {confirm === 'mail' ? <><p>Выбрано: {preview?.selected}. Доступно в Telegram: {preview?.eligible}. Удалённые заявки и неподключённые аккаунты исключены. Подтверждение создаст очередь на указанное время.</p><ul>{preview?.application_ids.map(id => <li key={id}>{name(data.content.applications?.find(app => app.id === id))}</li>)}</ul></> : <p>Действие будет применено к записи и связанным данным. Сохранённые ответы и назначения защищены сервером.</p>}
      <div className="organizer-actions"><button disabled={busy} onClick={() => setConfirm(undefined)}>Отмена</button><button disabled={busy || (confirm === 'mail' && !preview?.eligible)}
        onClick={() => void (confirm === 'mail' ? confirmMail() : confirm === 'delete' ? remove() : confirm === 'reload' ? refresh() : save())}>Подтвердить</button></div></Modal>}
    {blocker.state === 'blocked' && <Modal title="Есть несохранённые изменения" close={() => blocker.reset()}><p>Сохраните изменения или подтвердите уход.</p><div className="organizer-actions">
      <button onClick={() => blocker.reset()}>Остаться</button><button disabled={busy} onClick={() => blocker.proceed()}>Уйти без сохранения</button></div></Modal>}
  </section>
}

function ApplicationDetails({ data, draft }: { data: Data; draft: Values }) {
  const answers = Array.isArray(draft.answers) ? draft.answers.map(object) : []
  return <div className="organizer-editor"><h3>Анкета и предпочтения</h3><p>Не заполнено обязательных вопросов: {list(draft.missing_questions).length}</p>
    {answers.map(answer => <div key={text(answer.question_id)}><strong>{text(object(data.content.questions?.find(question => question.id === answer.question_id)).title) || `Вопрос №${text(answer.question_id)}`}</strong>
      <p>{Array.isArray(answer.value) ? answer.value.map(value => Array.isArray(value) ? value.join(', ') : text(value)).join(' / ') : text(answer.value)}</p></div>)}
    <h3>Понравившиеся персонажи</h3>{list(draft.likes).map(id => <p key={id}><Link to={`/organizer/${data.game!.id}/characters/${id}`}>{name(data.content.characters?.find(character => character.id === id))}</Link></p>)}</div>
}
