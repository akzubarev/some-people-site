import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { Component } from './Organizer'
import { gameDateInput, type OrganizerGame } from './data'
import { ApiError, api, json } from '../../shared/api/client'

vi.mock('../../shared/api/client', async importOriginal => ({ ...await importOriginal<typeof import('../../shared/api/client')>(),
  json: vi.fn(), api: vi.fn() }))
const original: OrganizerGame = { id: 1, title: 'Game', alias: 'game', revision: 'first', price: 1000, player_count: 75,
  description: 'Long', short_description: 'Short', location: 'Venue', year: 2028, start: '2028-02-01T15:00:00Z', end: null,
  vk: '', tg: '', open_applications: false, open_character_list: false }
let current: OrganizerGame
beforeEach(() => {
  current = { ...original }
  vi.mocked(json).mockReset(); vi.mocked(api).mockReset()
  HTMLDialogElement.prototype.showModal = function () { this.setAttribute('open', '') }
  HTMLDialogElement.prototype.close = function () { this.removeAttribute('open') }
})
afterEach(cleanup)
async function mount(path = '/organizer/1', canEdit = true) {
  const router = createMemoryRouter([{ path: '/organizer/:game_id?', Component, loader: ({ params }) => ({
    games: [current], game: params.game_id === '1' ? current : undefined, creating: params.game_id === 'new',
    permissions: { view: true, add: canEdit, change: canEdit }, timezone: 'Europe/Moscow',
  }) }], { initialEntries: [path] })
  render(<RouterProvider router={router} />)
  await screen.findByRole('heading', { level: 1 })
  return router
}
it('submits all fields and revision, preserving server times and updating the saved state', async () => {
  vi.mocked(json).mockImplementation(async (_path, payload) => {
    current = { ...current, ...payload as object, revision: 'second' }; return current as never
  })
  await mount()
  expect((screen.getByLabelText('Начало') as HTMLInputElement).value).toBe('2028-02-01T18:00')
  fireEvent.change(screen.getByLabelText('Название'), { target: { value: 'Edited' } })
  fireEvent.change(screen.getByLabelText('Взнос для новых заявок, ₽'), { target: { value: '6500' } })
  fireEvent.click(screen.getByRole('button', { name: 'Сохранить игру' }))
  await screen.findByText('Игра сохранена.')
  expect(json).toHaveBeenCalledWith('organizer/games/1/', expect.objectContaining({ title: 'Edited', price: 6500,
    player_count: 75, start: original.start, expected_revision: 'first', description: 'Long' }), 'PATCH')
})
it('keeps the draft after a conflict, and only reloads when explicitly confirmed', async () => {
  vi.mocked(json).mockRejectedValue(new ApiError(409, { detail: 'Changed elsewhere' }))
  vi.mocked(api).mockResolvedValue({ ...original, title: 'Server title', revision: 'second' })
  await mount()
  fireEvent.change(screen.getByLabelText('Название'), { target: { value: 'My draft' } })
  fireEvent.click(screen.getByRole('button', { name: 'Сохранить игру' }))
  await screen.findByText('Changed elsewhere')
  expect((screen.getByLabelText('Название') as HTMLInputElement).value).toBe('My draft')
  expect((screen.getByRole('button', { name: 'Сохранить игру' }) as HTMLButtonElement).disabled).toBe(true)
  fireEvent.click(screen.getByRole('button', { name: 'Загрузить актуальные данные' }))
  fireEvent.click(screen.getByRole('button', { name: 'Продолжить без сохранения' }))
  await waitFor(() => expect((screen.getByLabelText('Название') as HTMLInputElement).value).toBe('Server title'))
})
it('protects edits during navigation and supports cancelling departure', async () => {
  const router = await mount()
  fireEvent.change(screen.getByLabelText('Название'), { target: { value: 'My draft' } })
  fireEvent.click(screen.getByRole('link', { name: 'Все игры' }))
  await screen.findByRole('dialog', { name: 'Есть несохранённые изменения' })
  fireEvent.click(screen.getByRole('button', { name: 'Остаться' }))
  expect(router.state.location.pathname).toBe('/organizer/1')
  expect((screen.getByLabelText('Название') as HTMLInputElement).value).toBe('My draft')
  fireEvent.click(screen.getByRole('link', { name: 'Все игры' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Продолжить без сохранения' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/organizer'))
})
it('offers read-only content without a save control', async () => {
  await mount('/organizer/1', false)
  expect(screen.queryByRole('button', { name: 'Сохранить игру' })).toBeNull()
  expect((screen.getByLabelText('Название').closest('fieldset') as HTMLFieldSetElement).disabled).toBe(true)
})
it('creates with closed publication and navigates to the stable ID', async () => {
  vi.mocked(json).mockImplementation(async (_path, payload) => {
    current = { ...current, ...payload as object }; return current as never
  })
  const router = await mount('/organizer/new')
  fireEvent.change(screen.getByLabelText('Название'), { target: { value: 'New' } })
  fireEvent.change(screen.getByLabelText('Алиас в адресе страницы'), { target: { value: 'new-game' } })
  fireEvent.click(screen.getByRole('button', { name: 'Создать игру' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/organizer/1'))
  expect(json).toHaveBeenCalledWith('organizer/games/', expect.objectContaining({ title: 'New',
    open_applications: false, open_character_list: false }), 'POST')
})
it('uses the game time zone rather than the browser time zone', () => {
  expect(gameDateInput('2028-02-01T15:30:00Z', 'Europe/Moscow')).toBe('2028-02-01T18:30:00')
})
