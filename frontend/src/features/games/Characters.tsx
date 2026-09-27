import { Form, useLoaderData, useParams, useSearchParams, useNavigation, useSubmit } from 'react-router'
import type { charactersLoader } from '../../app/data'
import { CharacterCard } from './CharacterCard'

export function Component() {
  const { characters, tags } = useLoaderData<typeof charactersLoader>()
  const alias = useParams().game_alias!
  const [params, setParams] = useSearchParams()
  const navigation = useNavigation()
  const submit = useSubmit()
  return <main className="characters-page">
    <Form className="filters" method="get" key={params.toString()} onBlur={event => {
      if (event.relatedTarget instanceof Element && event.currentTarget.contains(event.relatedTarget)) return
      if (event.target instanceof HTMLInputElement && event.target.type === 'search') void submit(event.currentTarget)
    }}>
      <label><span className="sr-only">Поиск</span><input type="search" name="search" placeholder="Поиск по персонажам" defaultValue={params.get('search') || ''} /></label>
      <input type="hidden" name="tag" value={params.get('tag') || ''} />
      <div className="filter-tags" aria-label="Теги"><span>Тэги:</span>{tags.map(tag => <button key={tag.id} className="tag" type="button"
        style={{ color: params.get('tag') === tag.name ? 'white' : tag.color || undefined, borderColor: tag.color || undefined,
          backgroundColor: params.get('tag') === tag.name ? tag.color || undefined : 'transparent' }}
        aria-pressed={params.get('tag') === tag.name} onClick={event => {
          const next = new URLSearchParams(params)
          next.set('search', String(new FormData(event.currentTarget.form!).get('search') || ''))
          if (params.get('tag') === tag.name) next.delete('tag')
          else next.set('tag', tag.name)
          void setParams(next)
        }}>{tag.name}</button>)}</div>
    </Form>
    <h1>Персонажи</h1>
    <div className="character-results" aria-busy={navigation.state !== 'idle'}>
      {!characters.length && <p>Персонажей не найдено.</p>}
      {characters.map(character => <CharacterCard key={character.id} character={character} alias={alias} />)}
    </div>
  </main>
}
