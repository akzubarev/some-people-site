import { useState } from 'react'
import { Link, useLoaderData } from 'react-router'
import type { gameLoader } from '../../app/data'
import { useRoot } from '../../app/Shell'
import { gameImages, whaleLogo } from '../../shared/assets'
import whaleHalf from '../../assets/images/logo/whales-half.png'
import { Icon, LockedDialog } from '../../shared/Navigation'
import { publicLink } from '../../shared/api/client'

function dateRange(start: string | null, end: string | null, year: number | null) {
  if (!start || !end) return year ? String(year) : ''
  const a = new Date(start), b = new Date(end)
  const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
  return a.getDate() + (a.getMonth() === b.getMonth() ? '-' : ' ' + months[a.getMonth()] + ' - ') + b.getDate() + ' ' + months[b.getMonth()] + ' ' + year
}
export function Component() {
  const { game } = useLoaderData<typeof gameLoader>()
  const { user, games } = useRoot()
  const [locked, setLocked] = useState('')
  const other = games.find(other => other.alias !== game.alias)
  const links = [
    { title: 'Заявка', to: '/account/' + game.alias + '/application', locked: !user?.mg && !game.open_applications, message: 'Заявки еще/уже не принимаются' },
    { title: 'Сетка ролей', to: '/game/' + game.alias + '/roles', locked: !user?.mg && !game.open_character_list, message: 'Сетка ролей еще не открыта' },
  ]
  return <main className={'hero hero--' + game.alias} style={{ backgroundImage: 'url(' + gameImages(game.alias).background + ')' }}>
    <h1>{game.title}</h1>
    <div className="hero-band">
      <div className="hero-description"><p className="lead preserve">{game.short_description}</p>
        <ul className="facts"><li>{dateRange(game.start, game.end, game.year)}</li><li>{game.location}</li><li>{game.player_count} чел</li></ul>
      </div>
      <div className="hero-navigation"><div className="hero-links-logo">
        <nav className="hero-links" aria-label="Об игре">
          {links.map(link => link.locked
            ? <button key={link.title} className="locked" onClick={() => setLocked(link.message)}>{link.title}<Icon name="common/lock" /></button>
            : <Link key={link.title} to={link.to}>{link.title}</Link>)}
          {publicLink(game.vk, 'vk') && <a href={publicLink(game.vk, 'vk')} target="_blank" rel="noreferrer">Группа ВК</a>}
        </nav>
        {game.alias === 'whales' && <><img className="whale-logo" src={whaleLogo} alt="" />
          <img className="whale-half" src={whaleHalf} alt="" /></>}
      </div>
      {other && <Link className="other-games" to={'/game/' + other.alias + '/about'} aria-label={'Какие-то игры: ' + other.title}>
        <span>Какие-то<br />игры</span><Icon name="common/arrow" /></Link>}
      </div>
    </div>
    {locked && <LockedDialog title={locked} onClose={() => setLocked('')} />}
  </main>
}
