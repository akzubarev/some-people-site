import { Link, useFetcher } from 'react-router'
import { useRoot } from '../../app/Shell'
import type { ActionResult } from '../../app/data'
import type { Character } from '../../shared/api/types'
import { gameImages } from '../../shared/assets'
import { Errors, Picture, SocialLinks } from '../../shared/ui'
import { Icon } from '../../shared/Navigation'
import { PendingButton } from '../../shared/Loading'
import { hasGameEnded } from '../../shared/gameDates'

export function CharacterCard({ character, alias, personal = false }: {
  character: Character; alias: string; personal?: boolean
}) {
  const { user, games } = useRoot()
  const showVacancy = !hasGameEnded(games.find(game => game.alias === alias))
  const fetcher = useFetcher<ActionResult>()
  const liked = user?.likes.includes(character.id)
  const heart = <Icon name={'roles/heart-' + (liked ? 'filled' : 'unfilled')} />
  const like = showVacancy && !character.player && !personal && (user ? <fetcher.Form method="post" action={'/game/' + alias + '/roles'}>
    <input type="hidden" name="character_id" value={character.id} />
    <input type="hidden" name="like" value={String(!liked)} />
    <PendingButton className="like" pending={fetcher.state !== 'idle'} aria-pressed={liked}
      aria-label={(liked ? 'Убрать из избранного: ' : 'В избранное: ') + character.name}>{heart}</PendingButton>
    <Errors error={fetcher.data?.error} />
  </fetcher.Form> : <Link className="like" aria-label={'Войти, чтобы выбрать: ' + character.name} title="Сначала нужно подать заявку"
    to={'/sign-in?next=' + encodeURIComponent('/game/' + alias + '/roles')}>{heart}</Link>)
  return <article className={'character' + (personal ? ' character--personal' : '')} id={'character-' + character.id}>
    {!personal && <div className="character-mobile-title"><span>{character.alias}</span><div>
      <h3>{character.name}</h3>
      {character.player ? <details className="player-popup"><summary>{character.player.username}</summary><SocialLinks player={character.player} /></details> : showVacancy && <span>Свободно</span>}
    </div></div>}
    <div className="character-main"><div className="character-portrait"><div className="picture-frame">
      <Picture src={character.image} fallback={gameImages(alias).character} alt={character.name} className="character-picture" />
      <span className="picture-caption">{character.name_eng}</span>
    </div></div>
    <div className="character-description"><h3>{character.name}{character.alias && ', ' + character.alias}</h3>
      <p className="preserve">{character.description}</p>
      {personal && <Link className="role-return" to={'/game/' + alias + '/roles'}>→ Перейти в сетку</Link>}
      <div className="character-mobile-like">{like}</div>
    </div></div>
    {!personal && <div className="character-player"><span>{character.player?.username || (showVacancy ? 'Свободно' : '')}</span>
      {character.player && <SocialLinks player={character.player} />}{like}
    </div>}
  </article>
}
