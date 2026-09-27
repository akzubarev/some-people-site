import type { ComponentProps } from 'react'
import { brand } from './assets'

export function Spinner() {
  return <span className="spinner" aria-hidden="true" />
}

export function Loading({ label = 'Загрузка…', variant = 'inline' }: {
  label?: string; variant?: 'inline' | 'page' | 'navigation'
}) {
  return <div className={'loading loading--' + variant} role="status" aria-live="polite">
    {variant === 'page' && <img className="loading-brand" src={brand} alt="" />}
    <span className="loading-message"><Spinner />{label}</span>
  </div>
}

export function PageLoading() {
  return <main className="loading-page" aria-label="Какие-то люди"><Loading variant="page" /></main>
}

export function PendingButton({ pending, children, disabled, className = '', type = 'submit', ...props }:
  ComponentProps<'button'> & { pending: boolean }) {
  return <button {...props} type={type} className={'pending-button ' + className}
    disabled={disabled || pending} aria-busy={pending}>
    <span className="pending-button-icon">{pending && <Spinner />}</span>{children}
  </button>
}
