import { useLoaderData } from 'react-router'
import type { mgLoader } from '../../app/data'
import { Picture, SocialLinks } from '../../shared/ui'
import { avatar } from '../../shared/assets'
import { mgData } from './masterProfiles'

export function Component() {
  const players = useLoaderData<typeof mgLoader>()
  const sorted = [...players].sort((a, b) => (mgData[a.username]?.idx || 99) - (mgData[b.username]?.idx || 99))
  const sections = [
    { title: "Гм'ы", players: sorted.filter(p => mgData[p.username]?.idx <= 2) },
    { title: 'Сюжетный блок', players: sorted.filter(p => !mgData[p.username] || mgData[p.username].idx > 2) },
    { title: 'Арт-блок', players: [] }, { title: 'Игротехи', players: [] },
  ]
  return <main className="masters-page"><h1>МГ «Какие-то Люди»</h1>
    {sections.map(section => <section className="masters-section" key={section.title}><h2>{section.title}</h2>
      <div className="master-list">{section.players.map(player => {
        const master = mgData[player.username]
        return <div key={player.username}><article className="master">
          <Picture src={master?.image || player.avatar} fallback={avatar} alt={master?.name || player.username} />
          <div><h3>{master ? master.name + ' — ' + master.status : player.username}</h3>
            {master ? <p className="preserve">{master.description}</p> : <SocialLinks player={player} />}
          </div></article>
          <div className="master-footer">🍅 Сайт написан <a href="https://github.com/akzubarev/some-people-site" target="_blank" rel="noreferrer">@akzubarev</a>, можете написать <a href="https://t.me/Package_Man" target="_blank" rel="noreferrer">мне</a> за исходниками</div>
        </div>
      })}</div>
    </section>)}
  </main>
}
