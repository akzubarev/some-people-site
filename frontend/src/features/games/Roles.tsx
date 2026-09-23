import { useState } from 'react'
import { Link, useLoaderData, useParams } from 'react-router'
import type { rolesLoader } from '../../app/data'
import type { Group } from '../../shared/api/types'
import { gameImages, groupImage } from '../../shared/assets'
import { Drawer, Icon } from '../../shared/Navigation'
import { CharacterCard } from './CharacterCard'

export function visibleGroups(groups: Group[]): Group[] {
  return groups.filter(group => !group.hidden).flatMap(group => [
    group, ...visibleGroups(group.subgroups),
  ]).sort((a, b) => a.order - b.order)
}
const charactersOf = (group: Group) => [...new Map([...group.characters, ...group.members].map(character => [character.id, character])).values()]
function GroupLinks({ groups, family, onSelect }: { groups: Group[]; family: boolean; onSelect: () => void }) {
  return <>{groups.filter(group => !group.hidden).map(group => {
    const children = visibleGroups(group.subgroups).filter(child => child.family === family && charactersOf(child).length)
    if (!charactersOf(group).length && !children.length) return null
    const link = group.family === family && <a href={'#' + encodeURIComponent(group.name)} onClick={onSelect}>{group.name}</a>
    return children.length ? <details key={group.id} open><summary>{link || group.name}</summary>
      <div className="subgroup-links"><GroupLinks groups={group.subgroups} family={family} onSelect={onSelect} /></div></details>
      : link && <div className="group-link" key={group.id}>{link}</div>
  })}</>
}
export function Component() {
  const groups = useLoaderData<typeof rolesLoader>()
  const alias = useParams().game_alias!
  const [family, setFamily] = useState(false)
  const [drawer, setDrawer] = useState(false)
  const visible = visibleGroups(groups).filter(group => group.family === family && charactersOf(group).length)
  const groupNav = <div className="group-navigation">
    <Link className="back-link" to={'/game/' + alias + '/about'}><Icon name="common/arrow" />Назад</Link><h1>Сетка ролей</h1>
    <div className="group-navigation-scroll"><div className="tabs"><div>По <button aria-pressed={!family} onClick={() => setFamily(false)}>занятости</button> /</div>
      <button aria-pressed={family} onClick={() => setFamily(true)}>семьям</button></div>
      <nav aria-label="Группы"><GroupLinks groups={groups} family={family} onSelect={() => setDrawer(false)} /></nav>
    </div>
  </div>
  return <main className="roles-page">
    <img className="roles-background" src={gameImages(alias).header} alt="" />
    <div className="roles-stripe roles-stripe--navigation" /><div className="roles-stripe roles-stripe--characters" /><div className="roles-stripe roles-stripe--players" />
    <aside className="roles-sidebar">{groupNav}</aside>
    {drawer && <Drawer title="Группы" onClose={() => setDrawer(false)}>{groupNav}</Drawer>}
    <div className="role-content">
      {!visible.length && <><button className="mobile-only" onClick={() => setDrawer(true)}>Группы</button><p>Опубликованных групп пока нет.</p></>}
      {visible.map(group => <section key={group.id} id={group.name} className="group">
        <div className="group-title">{groupImage(alias, group.name) && <img src={groupImage(alias, group.name)} alt="" />}
          <button className="group-menu icon-button" aria-label="Открыть группы" onClick={() => setDrawer(true)}><Icon name="common/arrow" /></button>
          <div><h2>{group.name}</h2>
          {group.description && !/^\s*lorem ipsum\b/i.test(group.description) && <p className="preserve">{group.description}</p>}</div></div>
        <div className="group-characters">{charactersOf(group).map(character => <CharacterCard key={character.id} character={character} alias={alias} />)}</div>
      </section>)}
    </div>
  </main>
}
