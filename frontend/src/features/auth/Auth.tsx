import { useState, type CSSProperties } from 'react'
import { Form, Link, useActionData, useLocation, useNavigation, useSearchParams } from 'react-router'
import type { ActionResult } from '../../app/data'
import { Errors } from '../../shared/ui'
import { PendingButton } from '../../shared/Loading'
import { Icon } from '../../shared/Navigation'
import { brand } from '../../shared/assets'
import { safeNext } from '../../shared/api/client'

function Password({ signup, confirm = false }: { signup: boolean; confirm?: boolean }) {
  const [visible, setVisible] = useState(false)
  const label = confirm ? 'Повторите пароль' : 'Пароль'
  return <label><span className={signup ? '' : 'sr-only'}>{label}</span><span className="password-field">
    <input name={confirm ? 'password_confirm' : 'password'} type={visible ? 'text' : 'password'}
      placeholder={label} autoComplete={signup ? 'new-password' : 'current-password'} required />
    <button type="button" aria-label={visible ? 'Скрыть пароль' : 'Показать пароль'} aria-pressed={visible} onClick={() => setVisible(!visible)}>
      <Icon name={'auth/eye' + (visible ? '-off' : '')} /></button>
  </span></label>
}
export function Component() {
  const { pathname } = useLocation()
  const signup = pathname === '/sign-up'
  const signout = pathname === '/sign-out'
  const result = useActionData<ActionResult>()
  const navigation = useNavigation()
  const [params] = useSearchParams()
  return <main className="auth-page"><div className="auth-background" style={{ '--logo': 'url(' + JSON.stringify(brand) + ')' } as CSSProperties} />
    <section className="auth"><h1>{signout ? 'Выйти из аккаунта?' : 'Авторизация'}</h1>
    <Form method="post" key={pathname}>
      <input type="hidden" name="next" value={safeNext(params.get('next'))} />
      {!signout && <div className={'auth-fields' + (signup ? ' signup' : '')}>
        {signup ? <>
          <label>Имя<input name="first_name" placeholder="Имя" autoComplete="given-name" required maxLength={100} /></label>
          <label>Фамилия<input name="last_name" placeholder="Фамилия" autoComplete="family-name" required maxLength={100} /></label>
          <label>Никнейм<input name="username" placeholder="Никнейм" autoComplete="username" required maxLength={30} /></label>
          <label>Эл. почта<input name="email" aria-label="Email" placeholder="email" type="email" autoComplete="email" required /></label>
        </> : <label><span className="sr-only">Email или никнейм</span><input name="login_field" placeholder="Email / Никнейм" autoComplete="username" required /></label>}
        <Password signup={signup} />{signup && <Password signup confirm />}
      </div>}
      <Errors error={result?.error} />
      <div className="auth-actions">
        {!signout && <Link to={(signup ? '/sign-in' : '/sign-up') + '?next=' + encodeURIComponent(safeNext(params.get('next')))}>
          {signup ? 'Войти' : 'Зарегистрироваться'}</Link>}
        <PendingButton pending={navigation.state !== 'idle'}>{signout ? 'Выйти' : signup ? 'Зарегистрироваться' : 'Войти'}</PendingButton>
      </div>
    </Form>
    <Link to="/">Обратно на главную</Link>
  </section></main>
}
