import { describe, expect, it } from 'vitest'
import { hasGameEnded } from './gameDates'
import type { Game } from './api/types'

const now = new Date('2026-09-25T12:00:00Z')
const game = (end: string | null, year: number | null) => ({ end, year }) as Game
describe('past-game availability', () => {
  it('uses the end timestamp, not registration availability or the start date', () => {
    expect(hasGameEnded(game('2026-09-25T11:59:59Z', 2026), now)).toBe(true)
    expect(hasGameEnded(game('2026-09-26T00:00:00Z', 2020), now)).toBe(false)
  })
  it('uses an earlier year when the end date is missing', () => {
    expect(hasGameEnded(game(null, 2023), now)).toBe(true)
    expect(hasGameEnded(game(null, 2026), now)).toBe(false)
  })
  it('does not classify undated or missing games as past', () => {
    expect(hasGameEnded(game(null, null), now)).toBe(false)
    expect(hasGameEnded(undefined, now)).toBe(false)
  })
})
