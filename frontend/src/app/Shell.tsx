import { useEffect, useState } from 'react'
import { Link, Outlet, ScrollRestoration, useLoaderData, useLocation, useNavigation, useRouteLoaderData, useRevalidator } from 'react-router'
import type { rootLoader } from './data'
import { avatar } from '../shared/assets'
import { Brand, Drawer, Icon, LockedDialog } from '../shared/Navigation'
import { Picture } from '../shared/ui'
import { Loading } from '../shared/Loading'

export function useRoot() { return useRouteLoaderData<typeof rootLoader>('root')! }
export function Shell() {
  const { user } = useLoaderData<typeof rootLoader>()
  const [drawer, setDrawer] = useState(false)
  const [locked, setLocked] = useState(false)
  const { pathname } = useLocation()
  const authPage = /^\/sign(?:-|$)/.test(pathname)
  const navigation = useNavigation()
  const revalidator = useRevalidator()
  useEffect(() => {
    const refresh = () => { if (revalidator.state === 'idle') void revalidator.revalidate() }
    const channel = typeof BroadcastChannel !== 'undefined' ? new BroadcastChannel('some-people-session') : null
    if (channel) channel.onmessage = refresh
    window.addEventListener('focus', refresh)
    return () => { channel?.close(); window.removeEventListener('focus', refresh) }
  }, [revalidator])
  const menu = <nav className="site-menu" aria-label="Основное меню">
    {['Новичкам', 'МГ'].map(label => <button key={label} onClick={() => setLocked(true)}>{label}<Icon name="common/lock" /></button>)}
  </nav>
  return <>
    <a className="skip-link" href="#main">К содержимому</a>
    {!authPage && <header className="site-header"><div className="header-row">
      <button className="header-menu icon-button" aria-label="Открыть меню" onClick={() => setDrawer(true)}><Icon name="common/menu" /></button>
      <Brand />{menu}
      <Link to="/account/whales/application" aria-label={user ? 'Личный кабинет' : 'Войти'} className="header-avatar">
        <Picture src={user?.avatar} fallback={avatar} alt="" className="avatar" /></Link>
    </div></header>}
    {drawer && <Drawer title="Основное меню" onClose={() => setDrawer(false)}>{menu}</Drawer>}
    {locked && <LockedDialog title="Раздел в разработке" onClose={() => setLocked(false)} />}
    {navigation.state !== 'idle' && <Loading variant="navigation"
      label={navigation.formMethod && navigation.formMethod.toLowerCase() !== 'get' ? 'Сохраняем…' : 'Загрузка…'} />}
    <div id="main" aria-busy={navigation.state !== 'idle'}><Outlet /></div>
    <ScrollRestoration />
  </>
}
