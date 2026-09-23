import { useState, type ReactNode } from 'react'
import { Link, NavLink } from 'react-router'
import { useRoot } from '../../app/Shell'
import { Drawer, Icon } from '../../shared/Navigation'
import { gameImages } from '../../shared/assets'

export function Unfilled({ count }: { count: number }) {
  return count > 0 ? <span className="unfilled" aria-label={'Не заполнено: ' + count}>{count}</span> : null
}
function AccountNav({ alias, onNavigate, unfilled }: { alias: string; onNavigate?: () => void; unfilled: number }) {
  const { games, user } = useRoot()
  return <div className="account-nav">
    <div className="account-nav-top"><Link className="back-link" to={'/game/' + alias + '/about'}><Icon name="common/arrow" />Назад</Link>
      <div className="account-nav-heading"><h2>Личный кабинет</h2><p className="account-name">{user?.first_name} {user?.last_name}</p></div>
      <nav aria-label="Кабинет">{games.filter(game => game.alias === alias).map(game => <details open key={game.id}>
        <summary>{game.title}</summary><div className="account-game-links">
          <NavLink onClick={onNavigate} to={'/account/' + alias + '/application'}>Заявка</NavLink>
          <NavLink onClick={onNavigate} to={'/account/' + alias + '/questionnaire'}>Опросник <Unfilled count={unfilled} /></NavLink>
        </div></details>)}</nav>
    </div>
    <div className="account-nav-bottom"><nav aria-label="Профиль"><NavLink to="/account/settings" aria-label="Настройки" onClick={onNavigate}>Профиль</NavLink>
      <Link to="/sign-out" onClick={onNavigate}>Выйти</Link></nav></div>
  </div>
}
export function AccountLayout({ alias, children, className = '', unfilled = 0 }: { alias: string; children: ReactNode; className?: string; unfilled?: number }) {
  const { user } = useRoot()
  const [drawer, setDrawer] = useState(false)
  return <main className="account-page"><img className="account-background" src={gameImages(alias).header} alt="" />
    <aside className="account-sidebar"><AccountNav alias={alias} unfilled={unfilled} /></aside>
    {drawer && <Drawer title="Личный кабинет" onClose={() => setDrawer(false)}><AccountNav alias={alias} unfilled={unfilled} onNavigate={() => setDrawer(false)} /></Drawer>}
    <div className="account-main"><div className="account-mobile-heading">
      <button className="icon-button" aria-label="Меню кабинета" onClick={() => setDrawer(true)}><Icon name="common/menu" /></button>
      <div><h2>Личный кабинет</h2><p className="account-name">{user?.first_name} {user?.last_name}</p></div>
    </div><section className={'account-content ' + className}>{children}</section></div>
  </main>
}
