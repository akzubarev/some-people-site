import { useState } from 'react'
import { isRouteErrorResponse, Link, useRouteError } from 'react-router'
import { ApiError, publicLink } from './api/client'
import type { PublicPlayer } from './api/types'

export function Picture({ src, fallback, alt, className = '' }: {
  src?: string | null; fallback: string; alt: string; className?: string
}) {
  const [failed, setFailed] = useState<string | null>(null)
  const safe = src && (/^\/(?!\/)/.test(src) || publicLink(src))
  return <img src={safe && failed !== src ? src : fallback} alt={alt} className={className}
    loading="lazy" onError={() => { if (src && failed !== src) setFailed(src) }} />
}
export function SocialLinks({ player }: { player: PublicPlayer }) {
  return <span className="social-links">
    {publicLink(player.vk, 'vk') && <a href={publicLink(player.vk, 'vk')} rel="noreferrer" target="_blank">VK</a>}
    {publicLink(player.telegram, 'tg') && <a href={publicLink(player.telegram, 'tg')} rel="noreferrer" target="_blank">TG</a>}
  </span>
}
export function Errors({ error }: { error?: Record<string, unknown> }) {
  if (!error) return null
  const labels: Record<string, string> = {
    username: 'Никнейм', first_name: 'Имя', last_name: 'Фамилия', email: 'Email',
    phone: 'Телефон', password: 'Пароль', avatar: 'Аватар', vk: 'ВКонтакте', login_field: 'Логин',
  }
  return <div role="alert" className="error">{Object.entries(error).map(([key, value]) =>
    <p key={key}>{labels[key] ? labels[key] + ': ' : key.startsWith('question_') ? 'Ответ: ' : ''}
      {Array.isArray(value) ? value.join(' ') : String(value)}</p>)}</div>
}
export function RouteError() {
  const error = useRouteError()
  const status = error instanceof ApiError ? error.status : isRouteErrorResponse(error) ? error.status : 500
  return <main className="panel error-page">
    <h1>{status === 404 ? 'Страница не найдена' : status === 403 ? 'Доступ закрыт' : 'Не удалось загрузить страницу'}</h1>
    <p>Проверьте адрес или попробуйте ещё раз.</p>
    <button onClick={() => window.location.reload()}>Повторить</button> <Link to="/">На главную</Link>
  </main>
}
