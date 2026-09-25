import { useEffect, useRef, type ReactNode, type CSSProperties } from 'react'
import { Link } from 'react-router'
import { brand } from './assets'

const icons = import.meta.glob<string>('../assets/images/icons/**/*.svg', { eager: true, query: '?url', import: 'default' })
export function Icon({ name, className = '' }: { name: string; className?: string }) {
  return <span aria-hidden="true" className={'icon ' + className}
    style={{ '--icon': 'url(' + JSON.stringify(icons['../assets/images/icons/' + name + '.svg']) + ')' } as CSSProperties} />
}
export function Brand({ onClick }: { onClick?: () => void }) {
  return <Link className="brand" to="/" onClick={onClick} aria-label="Какие-то люди — главная">Какие-то
    <span className="brand-mark" aria-hidden="true" style={{ maskImage: 'url(' + JSON.stringify(brand) + ')' }} />юди</Link>
}
export function Drawer({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null)
  useEffect(() => { const dialog = ref.current!; dialog.showModal(); return () => dialog.close() }, [])
  return <dialog ref={ref} className="drawer" aria-label={title} onCancel={onClose}>
    <Brand onClick={onClose} />
    <button className="drawer-close icon-button" aria-label="Закрыть меню" onClick={onClose}><Icon name="common/chevrone" /></button>
    {children}
  </dialog>
}
export function LockedDialog({ title, onClose }: { title: string; onClose: () => void }) {
  const ref = useRef<HTMLDialogElement>(null)
  useEffect(() => { const dialog = ref.current!; dialog.showModal(); return () => dialog.close() }, [])
  return <dialog ref={ref} className="locked-dialog" aria-label={title} onCancel={onClose}>
    <button className="dialog-close" aria-label="Закрыть" onClick={onClose}>×</button>
    <img src={icons['../assets/images/icons/common/lock-gradient.svg']} alt="" />
    <p>{title}</p><button className="button" onClick={onClose}>Ok</button>
  </dialog>
}
