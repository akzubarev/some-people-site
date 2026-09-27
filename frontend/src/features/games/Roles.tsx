import { useEffect, useState } from 'react'
import { Link, useLoaderData, useLocation, useParams } from 'react-router'
import type { rolesLoader } from '../../app/data'
import type { Group } from '../../shared/api/types'
import { gameImages, groupImage } from '../../shared/assets'
import { Drawer, Icon } from '../../shared/Navigation'
import { CharacterCard } from './CharacterCard'

const charactersOf = (group: Group) => [...new Map([...group.characters, ...group.members].map(character => [character.id, character])).values()]
function visibleTree(groups: Group[]): Group[] {
  return groups.filter(group => !group.hidden).map(group => ({ ...group, subgroups: visibleTree(group.subgroups) }))
    .filter(group => charactersOf(group).length || group.subgroups.length)
}
function GroupLink({ group, initiallyExpanded = false, onSelect }: { group: Group; initiallyExpanded?: boolean; onSelect: (name: string) => void }) {
  const [expanded, setExpanded] = useState(initiallyExpanded)
  const parent = group.subgroups.length > 0
  return <div>
    <div className={'group-link-row' + (parent ? ' group-link-parent' : ' group-link')}>
      {parent && <button type="button" className="group-toggle" aria-label={'Подгруппы: ' + group.name}
        aria-expanded={expanded} onClick={() => setExpanded(!expanded)}><span aria-hidden="true">▶</span></button>}
      <Link to={'#' + encodeURIComponent(group.name)} onClick={() => onSelect(group.name)}>{group.name}</Link>
    </div>
    {parent && expanded && <div className="subgroup-links">{group.subgroups.map(child =>
      <GroupLink key={child.id} group={child} onSelect={onSelect} />)}</div>}
  </div>
}
function GroupContent({ group, alias, onMenu }: { group: Group; alias: string; onMenu: () => void }) {
  const characters = charactersOf(group)
  return <section id={group.name} className="group-tree">
    {!!characters.length && <div className="group">
      <div className="group-title">{groupImage(alias, group.name) && <img src={groupImage(alias, group.name)} alt="" />}
        <button className="group-menu icon-button" aria-label="Открыть группы" onClick={onMenu}><Icon name="common/arrow" /></button>
        <div><h2>{group.name}</h2>
        {group.description && !/^\s*lorem ipsum\b/i.test(group.description) && <p className="preserve">{group.description}</p>}</div></div>
      <div className="group-characters">{characters.map(character => <CharacterCard key={character.id} character={character} alias={alias} />)}</div>
    </div>}
    {group.subgroups.map(child => <GroupContent key={child.id} group={child} alias={alias} onMenu={onMenu} />)}
  </section>
}
function scrollToGroup(name: string) {
  const element = document.getElementById(name)
  const container = document.querySelector('.role-content')
  if (element && container) container.scrollTo({
    top: container.scrollTop + element.getBoundingClientRect().top - container.getBoundingClientRect().top - 10,
  })
}
export function Component() {
  const groups = useLoaderData<typeof rolesLoader>()
  const alias = useParams().game_alias!
  const [family, setFamily] = useState(false)
  const [drawer, setDrawer] = useState(false)
  const { hash, key } = useLocation()
  // Vue exposes the category's children first, then its own characters, preserving the nested anchors.
  const visible = visibleTree(groups.filter(group => group.family === family).flatMap(group =>
    group.hidden ? [] : [...group.subgroups, { ...group, subgroups: [] }]))
  useEffect(() => {
    try { if (hash) scrollToGroup(decodeURIComponent(hash.slice(1))) } catch { /* Ignore malformed fragment URLs. */ }
  }, [hash, key, groups, family])
  const selectGroup = (name: string) => {
    setDrawer(false)
    requestAnimationFrame(() => scrollToGroup(name))
  }
  const groupNav = <div className="group-navigation">
    <Link className="back-link" to={'/game/' + alias + '/about'}><Icon name="common/arrow" />Назад</Link><h1>Сетка ролей</h1>
    <div className="group-navigation-scroll"><div className="tabs"><div>По <button aria-pressed={!family} onClick={() => setFamily(false)}>занятости</button> /</div>
      <button aria-pressed={family} onClick={() => setFamily(true)}>семьям</button></div>
      <nav aria-label="Группы" key={alias + ':' + family}>{visible.map((group, index) =>
        <GroupLink key={group.id} group={group} initiallyExpanded={index === 0} onSelect={selectGroup} />)}</nav>
    </div>
  </div>
  return <main className="roles-page">
    <img className="roles-background" src={gameImages(alias).header} alt="" />
    <div className="roles-stripe roles-stripe--navigation" /><div className="roles-stripe roles-stripe--characters" /><div className="roles-stripe roles-stripe--players" />
    <aside className="roles-sidebar">{groupNav}</aside>
    {drawer && <Drawer title="Группы" onClose={() => setDrawer(false)}>{groupNav}</Drawer>}
    <div className="role-content">
      {!visible.length && <><button className="mobile-only" onClick={() => setDrawer(true)}>Группы</button><p>Опубликованных групп пока нет.</p></>}
      {visible.map(group => <GroupContent key={group.id} group={group} alias={alias} onMenu={() => setDrawer(true)} />)}
    </div>
  </main>
}
