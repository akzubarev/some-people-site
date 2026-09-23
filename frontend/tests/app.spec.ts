import { test, expect, type Page } from '@playwright/test'
import type { Application, Game, Group, Question, User } from '../src/shared/api/types'

const games: Game[] = ['whales', 'frostpunk'].map((alias, index) => ({
  id: index + 1, alias, title: alias === 'whales' ? 'Киты' : 'Frostpunk',
  short_description: 'Какие-то люди делают игры', description: 'Описание игры',
  location: 'Полигон', start: null, end: null, year: 2026, vk: 'javascript:alert(1)', tg: null,
  open_applications: true, open_character_list: true, player_count: 1,
}))
const user: User = { id: 1, username: 'player', first_name: 'Test', last_name: 'Player', email: 'player@example.invalid',
  phone: null, avatar: null, vk: 'previous', telegram: null, uuid: 'synthetic', created_at: '', mg: false,
  likes: [], applications: {}, vk_public: true, tg_public: true }
const character = { id: 1, name: 'Инженер', name_eng: '', alias: 'engineer',
  description: 'Биография <script>alert(1)</script>', image: '/broken.png', player: null, tags: [] }
const group: Group = { id: 1, name: 'Администрация', alias: 'admin', hidden: false, family: false,
  description: 'Lorem ipsum placeholder', game: 2, parent: null, order: 1, characters: [character], members: [], subgroups: [] }
const questionTypes: Question['type'][] = ['line', 'paragraph', 'single_choice', 'multiple_choice', 'scale', 'matrix', 'matrix_checkbox']
const questions: Question[] = questionTypes.map((type, index) => ({
  id: index + 1, title: type, type, description: '', order: index + 1, required: true,
  choices: type.startsWith('matrix') ? [['A', 'B'], ['One', 'Two']] : ['A', 'B'],
}))

async function setup(page: Page, authenticated = false) {
  let currentUser: User | null = authenticated ? structuredClone(user) : null
  let application: Application | null = authenticated ? {
    id: 1, game: 2, character: null, status: 'pending', price: 100, payed: 0,
    answers: { values: {}, unfilled: questions.map(q => q.id) },
  } : null
  const writes: { path: string; body: Record<string, unknown> | string }[] = []
  await page.route(url => url.pathname.startsWith('/api/'), async route => {
    const request = route.request()
    const url = new URL(request.url())
    const path = url.pathname
    const method = request.method()
    let body: Record<string, unknown> = {}
    if (method !== 'GET') {
      expect(request.headers().authorization).toBeUndefined()
      expect(request.headers()['x-csrftoken']).toBe('synthetic-csrf')
      if (request.headers()['content-type']?.includes('application/json')) body = request.postDataJSON()
      writes.push({ path, body: Object.keys(body).length ? body : request.postData() || '' })
    }
    const send = (value: unknown, status = 200) => route.fulfill({ status, json: value })
    if (path === '/api/session/' || path === '/api/session/register/') {
      if (method === 'POST') currentUser = structuredClone(user)
      if (method === 'DELETE') currentUser = null
      return send({ user: currentUser, csrfToken: 'synthetic-csrf' })
    }
    if (path === '/api/games/') return send(games)
    if (path === '/api/games/groups/') return send([{
      ...group, subgroups: [{ ...group, id: 2, name: 'Hidden group', hidden: true,
        subgroups: [{ ...group, id: 3, name: 'Hidden descendant', characters: [{ ...character, name: 'Secret' }] }] }],
    }])
    if (path === '/api/games/characters/') return send(url.searchParams.get('search') === 'empty' ? [] : [character])
    if (path === '/api/games/tags/') return send([{ id: 1, name: 'A&B', color: 'red' }])
    if (path.startsWith('/api/games/')) return send(games.find(game => path === '/api/games/' + game.alias + '/'))
    if (path === '/api/questions/') return send(questions)
    if (path === '/api/applications/get/') return send(application || {})
    if (path.startsWith('/api/applications/')) {
      if (!application) application = { id: 1, game: 2, character: null, status: 'pending',
        price: 100, payed: 0, answers: { values: {}, unfilled: [] } }
      if (path.endsWith('/delete/')) application = { ...application, status: 'deleted' }
      else if (path.endsWith('/restore/')) application = { ...application, status: 'pending' }
      else for (const [key, value] of Object.entries(body)) if (key.startsWith('question_'))
        application.answers.values[key.slice(9)] = value as string
      return send(application)
    }
    if (path === '/api/users/like_character/') {
      currentUser = { ...currentUser!, likes: body.like ? [Number(body.character_id)] : [] }
      return send({ status: 'ok' })
    }
    if (path === '/api/users/update_me/') return send(currentUser)
    if (path === '/api/users/telegram_link/') return send({ url: 'https://t.me/Somepeopllarpebot?start=synthetic', code: 'synthetic', expires_in: 600 })
    return send({ detail: 'Unexpected endpoint' }, 404)
  })
  return { writes }
}

test('initial loading is accessible and respects reduced motion', async ({ page }) => {
  await setup(page)
  await page.emulateMedia({ reducedMotion: 'reduce' })
  let release!: () => void
  const waiting = new Promise<void>(resolve => { release = resolve })
  await page.route('**/api/session/', async route => { await waiting; await route.fallback() })
  await page.goto('/game/frostpunk/about', { waitUntil: 'domcontentloaded' })
  const status = page.getByRole('status')
  await expect(status).toHaveText('Загрузка…')
  await expect(status.locator('.spinner')).toHaveCSS('animation-name', 'none')
  await page.screenshot({ path: 'test-results/loading-' + test.info().project.name + '.png' })
  release()
  await expect(page.getByRole('heading', { name: 'Frostpunk' })).toBeVisible()
  await expect(status).toHaveCount(0)
})

test('navigation retains the page and clears loading after success and failure', async ({ page }) => {
  await setup(page)
  await page.goto('/game/frostpunk/about')
  await expect(page.getByRole('heading', { name: 'Frostpunk' })).toBeVisible()
  let release!: () => void
  const waiting = new Promise<void>(resolve => { release = resolve })
  await page.route('**/api/games/groups/**', async route => { await waiting; await route.fallback() })
  await page.getByRole('link', { name: 'Сетка ролей', exact: true }).click()
  await expect(page.getByRole('status')).toHaveText('Загрузка…')
  await expect(page.getByRole('heading', { name: 'Frostpunk' })).toBeVisible()
  await expect(page.locator('#main')).toHaveAttribute('aria-busy', 'true')
  await expect(page.getByRole('link', { name: 'Войти', exact: true })).toBeVisible()
  release()
  await expect(page.getByRole('heading', { name: 'Администрация' })).toBeVisible()
  await expect(page.getByRole('status')).toHaveCount(0)
  await expect(page.locator('#main')).toHaveAttribute('aria-busy', 'false')

  const failing = new Promise<void>(resolve => { release = resolve })
  await page.route('**/api/games/whales/', async route => {
    await failing
    await route.fulfill({ status: 500, json: { detail: 'Synthetic failure' } })
  })
  await page.getByRole('link', { name: 'Какие-то люди — главная' }).click()
  await expect(page.getByRole('status')).toHaveText('Загрузка…')
  release()
  await expect(page.getByRole('heading', { name: 'Не удалось загрузить страницу' })).toBeVisible()
  await expect(page.getByRole('status')).toHaveCount(0)
  await expect(page.locator('#main')).toHaveAttribute('aria-busy', 'false')
})

test('another navigation can cancel a slow page without leaving a loader behind', async ({ page }) => {
  await setup(page)
  await page.goto('/game/frostpunk/about')
  let release!: () => void
  const waiting = new Promise<void>(resolve => { release = resolve })
  await page.route('**/api/games/groups/**', async route => { await waiting; await route.fallback() })
  await page.getByRole('link', { name: 'Сетка ролей', exact: true }).click()
  await expect(page.getByRole('status')).toHaveText('Загрузка…')
  await page.getByRole('link', { name: 'Войти', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Авторизация', exact: true })).toBeVisible()
  release()
  await expect(page.getByRole('status')).toHaveCount(0)
  await expect(page.locator('#main')).toHaveAttribute('aria-busy', 'false')
})

test('local actions show pending feedback, prevent duplicates, and recover after failure', async ({ page }) => {
  await setup(page, true)
  await page.goto('/game/frostpunk/roles')
  let release!: () => void
  const waiting = new Promise<void>(resolve => { release = resolve })
  await page.route('**/api/users/like_character/', async route => {
    await waiting
    await route.fulfill({ status: 500, json: { detail: 'Synthetic failure' } })
  }, { times: 1 })
  const like = page.getByRole('button', { name: 'В избранное: Инженер', exact: true })
  await like.click()
  await expect(like).toBeDisabled()
  await expect(like).toHaveAttribute('aria-busy', 'true')
  await expect(like.locator('.spinner')).toBeVisible()
  await expect(page.getByRole('status')).toHaveCount(0)
  await expect(page.locator('#main')).toHaveAttribute('aria-busy', 'false')
  release()
  await expect(page.getByRole('alert')).toBeVisible()
  await expect(like).toBeEnabled()
  await expect(like).toHaveAttribute('aria-busy', 'false')
  await expect(like.locator('.spinner')).toHaveCount(0)
  await like.click()
  await expect(page.getByRole('button', { name: 'Убрать из избранного: Инженер' })).toHaveAttribute('aria-pressed', 'true')
})

test('public routes preserve game selection, hidden ancestors, safe text, and image fallbacks', async ({ page }) => {
  await setup(page)
  await page.goto('/game/frostpunk')
  await expect(page.getByRole('heading', { name: 'Frostpunk' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'ВКонтакте' })).toHaveCount(0)
  await page.getByRole('link', { name: 'Сетка ролей', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Администрация' })).toBeVisible()
  await expect(page.getByText('Hidden group')).toHaveCount(0)
  await expect(page.getByText('Hidden descendant')).toHaveCount(0)
  await expect(page.getByText('Lorem ipsum placeholder')).toHaveCount(0)
  await expect(page.getByText('Биография <script>alert(1)</script>')).toBeVisible()
  await expect(page.getByAltText('Инженер')).toHaveAttribute('src', /default.*png/)
  await page.screenshot({ path: 'test-results/roles-' + test.info().project.name + '.png', fullPage: true })
})
test('search and tags survive refresh and empty results can be reset', async ({ page }) => {
  await setup(page)
  await page.goto('/game/frostpunk/characters')
  await page.getByLabel('Поиск', { exact: true }).fill('empty')
  await page.getByRole('button', { name: 'A&B', exact: true }).click()
  await expect(page).toHaveURL(/search=empty/)
  await expect(page).toHaveURL(/tag=A%26B/)
  await expect(page.getByText('Персонажей не найдено.')).toBeVisible()
  await page.reload()
  await expect(page.getByLabel('Поиск', { exact: true })).toHaveValue('empty')
  await page.getByLabel('Поиск', { exact: true }).fill('')
  await page.getByLabel('Поиск', { exact: true }).press('Enter')
  await expect(page).not.toHaveURL(/search=empty/)
  await page.getByRole('button', { name: 'A&B', exact: true }).click()
  await expect(page.getByRole('heading', { name: /^Инженер/ })).toBeVisible()
})
test('protected routes return to the requested game after login and logout clears account data', async ({ page, baseURL }) => {
  await setup(page)
  await page.context().addCookies([{ name: 'auth_token', value: 'legacy-browser-token', url: baseURL! }])
  await page.goto('/account/frostpunk/application')
  expect((await page.context().cookies()).some(cookie => cookie.name === 'auth_token')).toBe(false)
  await page.getByLabel('Email или никнейм').fill('player')
  await page.getByLabel('Пароль', { exact: true }).fill('synthetic-password')
  await page.getByRole('button', { name: 'Войти', exact: true }).click()
  await expect(page).toHaveURL(/account\/frostpunk\/application/)
  await page.getByRole('button', { name: 'Подать заявку' }).click()
  await expect(page.getByRole('heading', { name: 'Заявка подана' })).toBeVisible()
  if (await page.getByRole('button', { name: 'Меню кабинета' }).isVisible()) await page.getByRole('button', { name: 'Меню кабинета' }).click()
  await page.getByRole('link', { name: 'Выйти', exact: true }).click()
  await page.getByRole('button', { name: 'Выйти', exact: true }).click()
  await expect(page.getByRole('link', { name: 'Войти', exact: true })).toBeVisible()
  expect(await page.evaluate(() => Object.keys(localStorage))).toEqual([])
})
test('likes revalidate the current user and can be removed', async ({ page }) => {
  await setup(page, true)
  await page.goto('/game/frostpunk/roles')
  await page.getByRole('button', { name: 'В избранное: Инженер', exact: true }).click()
  await expect(page.getByRole('button', { name: 'Убрать из избранного: Инженер' })).toHaveAttribute('aria-pressed', 'true')
  await page.getByRole('button', { name: 'Убрать из избранного: Инженер' }).click()
  await expect(page.getByRole('button', { name: 'В избранное: Инженер', exact: true })).toHaveAttribute('aria-pressed', 'false')
})
test('profile submits explicit clearing and unchecked consent and can issue a Telegram link', async ({ page }) => {
  const { writes } = await setup(page, true)
  await page.goto('/account/settings')
  await page.getByLabel('ВКонтакте', { exact: true }).first().fill('')
  await page.getByRole('checkbox', { name: 'ВКонтакте' }).uncheck()
  await page.getByRole('checkbox', { name: 'Телеграм', exact: true }).uncheck()
  await page.getByRole('button', { name: 'Сохранить профиль' }).click()
  await expect(page.getByText('Профиль сохранён.')).toBeVisible()
  const profile = String(writes.find(write => write.path.endsWith('/update_me/'))!.body)
  expect(profile).toContain('name="vk_public"\r\n\r\nfalse')
  expect(profile).toContain('name="tg_public"\r\n\r\nfalse')
  await page.getByRole('button', { name: 'Получить ссылку для подключения' }).click()
  await expect(page.getByRole('link', { name: 'Подключить Телеграм' })).toHaveAttribute('href', /start=synthetic/)
})
test('all seven questionnaire fields autosave with the backend answer shapes', async ({ page }) => {
  const { writes } = await setup(page, true)
  await page.goto('/account/frostpunk/questionnaire')
  await page.getByLabel('line *', { exact: true }).fill('short answer')
  await page.getByLabel('paragraph *', { exact: true }).fill('long answer')
  await page.getByRole('group', { name: 'single_choice *', exact: true }).getByLabel('A', { exact: true }).check()
  await page.getByRole('group', { name: 'multiple_choice *', exact: true }).getByLabel('B', { exact: true }).check()
  await page.getByRole('group', { name: 'scale *', exact: true }).getByLabel('A', { exact: true }).check()
  await page.getByRole('group', { name: 'matrix *', exact: true }).getByLabel('One: B', { exact: true }).check()
  await page.getByRole('group', { name: 'matrix_checkbox *', exact: true }).getByLabel('Two: A', { exact: true }).check()
  await expect(page.getByRole('status').filter({ hasText: 'Все изменения сохранены.' })).toBeVisible()
  const last = writes.filter(write => write.path.endsWith('/apply/')).at(-1)!.body
  expect(last).toMatchObject({ game_alias: 'frostpunk', question_1: 'short answer', question_2: 'long answer',
    question_3: 'A', question_4: ['B'], question_5: 'A', question_6: [['B'], []], question_7: [[], ['A']] })
  await page.reload()
  await expect(page.getByLabel('line *', { exact: true })).toHaveValue('short answer')
})
test('application delete and restore keep the route and state coherent', async ({ page }) => {
  await setup(page, true)
  await page.goto('/account/frostpunk/application')
  page.on('dialog', dialog => dialog.accept())
  await page.getByRole('button', { name: 'Удалить заявку' }).click()
  await expect(page.getByRole('heading', { name: 'Заявка удалена' })).toBeVisible()
  await page.getByRole('button', { name: 'Восстановить заявку' }).click()
  await expect(page.getByRole('heading', { name: 'Заявка подана' })).toBeVisible()
})

test('a failed autosave keeps edits and can be retried without changing games', async ({ page }) => {
  await setup(page, true)
  let failed = false
  await page.route(url => url.pathname === '/api/applications/apply/', async route => {
    if (!failed) { failed = true; return route.fulfill({ status: 503, json: { detail: 'Сервис временно недоступен.' } }) }
    return route.fallback()
  })
  await page.goto('/account/frostpunk/questionnaire')
  await page.getByLabel('line *', { exact: true }).fill('keep this answer')
  await expect(page.getByRole('alert')).toContainText('Сервис временно недоступен.')
  await page.getByRole('link', { name: 'Какие-то люди — главная' }).click()
  await expect(page.getByRole('alertdialog')).toBeVisible()
  await page.getByRole('button', { name: 'Остаться', exact: true }).click()
  await page.getByRole('button', { name: 'Повторить сохранение' }).click()
  await expect(page.getByText('Все изменения сохранены.', { exact: true })).toBeVisible()
  await expect(page).toHaveURL(/frostpunk\/questionnaire/)
  await page.reload()
  await expect(page.getByLabel('line *', { exact: true })).toHaveValue('keep this answer')
})

test('avatar cropping produces an upload on mobile as well as desktop', async ({ page }) => {
  const { writes } = await setup(page, true)
  await page.goto('/account/settings')
  await page.getByLabel('Аватар', { exact: true }).setInputFiles({
    name: 'avatar.png', mimeType: 'image/png',
    buffer: Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aVkUAAAAASUVORK5CYII=', 'base64'),
  })
  await expect(page.getByLabel('Предпросмотр аватара')).toBeVisible()
  await page.getByLabel('Масштаб', { exact: true }).fill('2')
  await page.getByRole('button', { name: 'Сохранить профиль' }).click()
  await expect(page.getByText('Профиль сохранён.')).toBeVisible()
  expect(String(writes.find(write => write.path.endsWith('/update_me/'))!.body)).toContain('filename="avatar.png"')
})

test('Vue layout is retained on the game landing page and role grid', async ({ page, isMobile }) => {
  await setup(page)
  await page.goto('/game/frostpunk/about')
  await expect(page.getByRole('heading', { name: 'Frostpunk' })).toBeVisible()
  const header = page.locator('.site-header')
  await expect(header).toHaveCSS('position', 'absolute')
  expect((await header.boundingBox())!.y).toBe(24)
  expect((await header.boundingBox())!.height).toBe(isMobile ? 40 : 56)
  await expect(page.locator('.brand-mark')).not.toHaveCSS('mask-image', 'none')
  await expect(page.locator('.hero')).toHaveCSS('height', page.viewportSize()!.height + 'px')
  const title = (await page.getByRole('heading', { name: 'Frostpunk' }).boundingBox())!
  if (isMobile) expect(title.y).toBe(80)
  else expect(title.y).toBeGreaterThan(page.viewportSize()!.height / 2)
  await expect(page.locator('footer')).toHaveCount(0)
  await page.getByRole('link', { name: 'Сетка ролей', exact: true }).click()
  await expect(page.locator('.role-content')).toHaveCSS('overflow-y', 'auto')
  await expect(page.locator('.character-picture')).not.toHaveCSS('object-fit', 'cover')
  if (isMobile) {
    await expect(page.locator('.roles-sidebar')).toBeHidden()
    await page.getByRole('button', { name: 'Открыть группы' }).click()
    await expect(page.getByRole('dialog', { name: 'Группы', exact: true })).toBeVisible()
    await page.getByRole('link', { name: 'Администрация', exact: true }).click()
    await expect(page.getByRole('dialog')).toHaveCount(0)
    await expect(page.getByRole('heading', { name: 'Администрация' })).toBeVisible()
    await page.getByRole('button', { name: 'Открыть меню', exact: true }).click()
    await expect(page.getByRole('dialog', { name: 'Основное меню' })).toBeVisible()
    await page.keyboard.press('Escape')
    await expect(page.getByRole('dialog')).toHaveCount(0)
  } else {
    await expect(page.locator('.roles-sidebar')).toBeVisible()
    const width = page.viewportSize()!.width
    const stripe = (await page.locator('.roles-stripe--characters').boundingBox())!
    expect(stripe.x).toBeCloseTo(width * .25, 0)
    expect(stripe.width).toBeCloseTo(width * .575, 0)
    await expect(page.locator('.character-player .like .icon')).not.toHaveCSS('mask-image', 'none')
  }
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
})

test('auth retains the original standalone background and card without the site header', async ({ page }) => {
  await setup(page)
  await page.goto('/sign-in')
  await expect(page.getByRole('heading', { name: 'Авторизация' })).toBeVisible()
  await expect(page.locator('.site-header')).toHaveCount(0)
  await expect(page.locator('.auth-background')).not.toHaveCSS('mask-image', 'none')
  await expect(page.locator('.auth')).toHaveCSS('background-color', 'rgba(0, 0, 0, 0.4)')
  await expect(page.getByRole('link', { name: 'Обратно на главную' })).toBeVisible()
})
