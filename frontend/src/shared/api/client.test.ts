import { afterEach, expect, it, vi } from 'vitest'
import { api, ApiError, json, publicLink, query, safeNext, session } from './client'

afterEach(() => vi.unstubAllGlobals())
it('limits navigation to same-origin paths and social links to web URLs', () => {
  for (const target of ['//evil.example', '/\\evil.example', 'https://evil.example', '/\nevil']) {
    expect(safeNext(target)).toBe('/account/')
  }
  expect(safeNext('/account/frostpunk/application')).toBe('/account/frostpunk/application')
  expect(publicLink('javascript:alert(1)')).toBeUndefined()
  expect(publicLink('https://user:password@example.com')).toBeUndefined()
  expect(publicLink('@person', 'tg')).toBe('https://t.me/person')
  expect(query('games/', { search: 'A&B?#', tag: null })).toBe('games/?search=A%26B%3F%23')
})
it('keeps private requests out of caches and sends CSRF for writes', async () => {
  const fetcher = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ user: null, csrfToken: 'masked-token' })))
    .mockResolvedValueOnce(new Response('{}'))
  vi.stubGlobal('fetch', fetcher)
  await session()
  await json('users/update_me/', { vk: '' }, 'PUT')
  const [, options] = fetcher.mock.calls[1]
  expect(options.credentials).toBe('same-origin')
  expect(options.cache).toBe('no-store')
  expect(options.headers.get('X-CSRFToken')).toBe('masked-token')
  expect(options.headers.has('Authorization')).toBe(false)
})
it('preserves field errors and cancellation', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ username: ['Taken'] }), { status: 400 })))
  await expect(api('users/')).rejects.toMatchObject({ status: 400, fields: { username: ['Taken'] } })
  const abort = new DOMException('Aborted', 'AbortError')
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(abort))
  await expect(api('games/')).rejects.toBe(abort)
  expect(new ApiError(503, {}).status).toBe(503)
})
