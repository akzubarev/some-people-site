import type { components } from './schema'

export type PublicPlayer = components['schemas']['UserPublic']
export type User = components['schemas']['UserPrivate']
export type Game = components['schemas']['Game']
export type Tag = components['schemas']['Tag']
export type Character = components['schemas']['Character']
export type Group = components['schemas']['Group']
export type Question = components['schemas']['Question']
export type ApplicationSummary = components['schemas']['ApplicationPublic']
export type Application = components['schemas']['ApplicationPrivate']
export type Answer = Application['answers']['values'][string]
export type Session = components['schemas']['Session']
