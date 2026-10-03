import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { GoogleAuth } from './GoogleAuth'
import { api, authenticate, json } from '../../shared/api/client'

vi.mock('../../shared/api/client', () => ({ api: vi.fn(), authenticate: vi.fn(), json: vi.fn(), safeNext: () => '/account/' }))
const apiMock = vi.mocked(api)
const jsonMock = vi.mocked(json)
const authenticateMock = vi.mocked(authenticate)
const renderButton = vi.fn()
const initialize = vi.fn()
const cancel = vi.fn()
beforeEach(() => {
  vi.clearAllMocks()
  apiMock.mockResolvedValue({ enabled: true, linked: false, can_unlink: false })
  jsonMock.mockResolvedValue({ nonce: 'synthetic-nonce', client_id: 'synthetic-client', expires_in: 300 })
  window.google = { accounts: { id: { initialize, renderButton, cancel } } }
})
afterEach(() => { cleanup(); delete window.google })
function mount(linking = false) { return render(<MemoryRouter><GoogleAuth linking={linking} /></MemoryRouter>) }
it('hides Google when disabled without changing password controls', async () => {
  apiMock.mockResolvedValue({ enabled: false, linked: false, can_unlink: false })
  mount()
  await waitFor(() => expect(apiMock).toHaveBeenCalled())
  expect(screen.queryByRole('button')).toBeNull()
})
it('binds the Google button to the server nonce and cancels without authenticating', async () => {
  mount()
  fireEvent.click(await screen.findByText('Войти или зарегистрироваться через Google'))
  await screen.findByText('Отменить попытку')
  expect(initialize).toHaveBeenCalledWith(expect.objectContaining({ nonce: 'synthetic-nonce', auto_select: false }))
  fireEvent.click(screen.getByText('Отменить попытку'))
  expect(jsonMock).toHaveBeenLastCalledWith('session/google/challenge/', { nonce: 'synthetic-nonce' }, 'DELETE')
  expect(authenticateMock).not.toHaveBeenCalled()
  expect(screen.getByText('Попытка отменена.')).toBeTruthy()
})
it('shows invalid credential errors and permits a fresh attempt', async () => {
  authenticateMock.mockRejectedValue(new Error('Invalid Google credential'))
  mount()
  fireEvent.click(await screen.findByText('Войти или зарегистрироваться через Google'))
  await screen.findByText('Отменить попытку')
  const callback = initialize.mock.calls[0][0].callback as (data: { credential: string }) => Promise<void>
  await callback({ credential: 'invalid' })
  expect(await screen.findByRole('alert')).toHaveProperty('textContent', 'Invalid Google credential')
  expect(authenticateMock).toHaveBeenCalledWith('session/google/', { nonce: 'synthetic-nonce', credential: 'invalid' })
})
it('requires password confirmation for linking and clears it after challenge issuance', async () => {
  mount(true)
  const start = await screen.findByText('Подключить Google') as HTMLButtonElement
  expect(start.disabled).toBe(true)
  fireEvent.change(screen.getByLabelText('Текущий пароль'), { target: { value: 'confirmation-password' } })
  fireEvent.click(start)
  await screen.findByText('Отменить попытку')
  expect(jsonMock).toHaveBeenCalledWith('session/google/challenge/', { purpose: 'link', password: 'confirmation-password' })
  expect(screen.getByLabelText('Текущий пароль')).toHaveProperty('value', '')
})
it('prevents Google-only accounts from unlinking', async () => {
  apiMock.mockResolvedValue({ enabled: true, linked: true, can_unlink: false })
  mount(true)
  await screen.findByText('Google — единственный способ входа. Его нельзя отключить, пока у аккаунта нет пароля.')
  expect(screen.queryByText('Отключить Google')).toBeNull()
})
it('unlinks using current password and preserves login', async () => {
  apiMock.mockResolvedValue({ enabled: true, linked: true, can_unlink: true })
  authenticateMock.mockResolvedValue({ csrfToken: 'new', user: null })
  mount(true)
  await screen.findByText('Отключить Google')
  fireEvent.change(screen.getByLabelText('Текущий пароль'), { target: { value: 'confirmation-password' } })
  fireEvent.click(screen.getByText('Отключить Google'))
  await screen.findByText('Google отключён. Вход по паролю сохранён.')
  expect(authenticateMock).toHaveBeenCalledWith('session/google/identity/', { password: 'confirmation-password' }, 'DELETE')
})
