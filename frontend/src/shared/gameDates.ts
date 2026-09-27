import type { Game } from './api/types'

export function hasGameEnded(game: Game | undefined, now = new Date()): boolean {
  if (!game) return false
  const end = game.end ? Date.parse(game.end) : NaN
  if (Number.isFinite(end)) return end < now.getTime()
  return typeof game.year === 'number' && game.year < now.getFullYear()
}
