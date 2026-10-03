import { useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'
import { api, authenticate, json, safeNext } from '../../shared/api/client'
import type { components } from '../../shared/api/schema'

type GoogleStatus = components['schemas']['GoogleStatus']
type Challenge = components['schemas']['ChallengeOutput']
interface GoogleAPI {
  initialize(options: { client_id: string; nonce: string; auto_select: boolean; callback: (result: { credential: string }) => void }): void
  renderButton(element: HTMLElement, options: { theme: string; size: string; text: string }): void
  cancel(): void
}
declare global { interface Window { google?: { accounts: { id: GoogleAPI } } } }
let scriptPromise: Promise<GoogleAPI> | undefined
export function loadGoogle(): Promise<GoogleAPI> {
  if (window.google) return Promise.resolve(window.google.accounts.id)
  if (!scriptPromise) scriptPromise = new Promise<GoogleAPI>((resolve, reject) => {
    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    const timer = window.setTimeout(() => fail(), 15000)
    const fail = () => { clearTimeout(timer); script.remove(); scriptPromise = undefined; reject(new Error('Не удалось загрузить Google. Попробуйте ещё раз.')) }
    script.onload = () => { clearTimeout(timer); if (window.google) resolve(window.google.accounts.id); else fail() }
    script.onerror = fail
    document.head.append(script)
  })
  return scriptPromise
}

export function GoogleAuth({ linking = false }: { linking?: boolean }) {
  const [status, setStatus] = useState<GoogleStatus>()
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [stage, setStage] = useState<'idle' | 'preparing' | 'ready' | 'submitting'>('idle')
  const button = useRef<HTMLDivElement>(null)
  const attempt = useRef<Challenge | null>(null)
  const generation = useRef(0)
  const [params] = useSearchParams()
  const destination = safeNext(params.get('next'))

  useEffect(() => {
    const controller = new AbortController()
    void api<GoogleStatus>('session/google/identity/', { signal: controller.signal }).then(setStatus)
      .catch(() => { if (!controller.signal.aborted && linking) setError('Не удалось проверить подключение Google.') })
    return () => controller.abort()
  }, [linking])

  function discard() {
    const previous = attempt.current
    attempt.current = null
    generation.current++
    window.google?.accounts.id.cancel()
    button.current?.replaceChildren()
    if (previous) void json('session/google/challenge/', { nonce: previous.nonce }, 'DELETE').catch(() => {})
  }
  useEffect(() => () => {
    // Invalidate the server challenge when leaving this screen.
    const previous = attempt.current
    attempt.current = null
    generation.current++
    window.google?.accounts.id.cancel()
    if (previous) void json('session/google/challenge/', { nonce: previous.nonce }, 'DELETE').catch(() => {})
  }, [])
  useEffect(() => {
    if (stage !== 'ready') return
    const timer = window.setTimeout(() => {
      discard(); setStage('idle'); setNotice('Срок попытки истёк. Начните заново.')
    }, (attempt.current?.expires_in || 300) * 1000)
    return () => clearTimeout(timer)
  }, [stage])

  async function start() {
    if (stage !== 'idle') return
    const current = ++generation.current
    setError(''); setNotice(''); setStage('preparing')
    try {
      const challenge = await json<Challenge>('session/google/challenge/', { purpose: linking ? 'link' : 'signin', ...(linking ? { password } : {}) })
      setPassword('')
      if (generation.current !== current) {
        void json('session/google/challenge/', { nonce: challenge.nonce }, 'DELETE').catch(() => {})
        return
      }
      attempt.current = challenge
      const google = await loadGoogle()
      if (generation.current !== current || !button.current) return
      google.initialize({ client_id: challenge.client_id, nonce: challenge.nonce, auto_select: false, callback: async result => {
        if (generation.current !== current || !attempt.current) return
        setStage('submitting')
        try {
          await authenticate('session/google/', { nonce: challenge.nonce, credential: result.credential })
          attempt.current = null
          if (generation.current !== current) return
          window.location.assign(linking ? '/account/settings' : destination)
        } catch (cause) {
          if (generation.current !== current) return
          discard(); setStage('idle'); setError(cause instanceof Error ? cause.message : 'Ошибка входа через Google.')
        }
      } })
      google.renderButton(button.current, { theme: 'outline', size: 'large', text: linking ? 'continue_with' : 'signin_with' })
      setStage('ready')
    } catch (cause) {
      if (generation.current !== current) return
      discard(); setStage('idle'); setError(cause instanceof Error ? cause.message : 'Ошибка подключения Google.')
    }
  }
  async function unlink() {
    setError(''); setStage('submitting')
    try {
      await authenticate('session/google/identity/', { password }, 'DELETE')
      setPassword(''); setStatus(previous => previous ? { ...previous, linked: false, can_unlink: false } : previous)
      setNotice('Google отключён. Вход по паролю сохранён.')
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Не удалось отключить Google.') }
    finally { setStage('idle') }
  }
  if (!status?.enabled && !status?.linked && !error) return null
  return <section className="google-auth" aria-label={linking ? 'Подключение Google' : 'Вход через Google'}>
    {linking && <><h2>Google</h2><p>{status?.linked ? 'Google подключён к этому аккаунту.' : 'Подключите Google для входа в этот аккаунт. Пароль сохранится.'}</p></>}
    {linking && status && (!status.linked || status.can_unlink) && <label>Текущий пароль<input type="password" value={password} onChange={event => setPassword(event.target.value)} autoComplete="current-password" disabled={stage !== 'idle'} /></label>}
    {status?.linked ? status.can_unlink
      ? <button type="button" className="profile-button profile-button--secondary" disabled={stage !== 'idle' || !password} onClick={() => void unlink()}>Отключить Google</button>
      : <p>Google — единственный способ входа. Его нельзя отключить, пока у аккаунта нет пароля.</p>
      : status?.enabled && <button type="button" className="profile-button profile-button--secondary" disabled={stage !== 'idle' || (linking && !password)} onClick={() => void start()}>{linking ? 'Подключить Google' : 'Войти или зарегистрироваться через Google'}</button>}
    <div ref={button} hidden={stage !== 'ready'} />
    {stage === 'ready' && <><p>Выберите Google-аккаунт. Если закрыли окно Google, можно повторить попытку.</p><button type="button" onClick={() => { discard(); setStage('idle'); setNotice('Попытка отменена.') }}>Отменить попытку</button></>}
    {(stage === 'preparing' || stage === 'submitting') && <p role="status">{stage === 'preparing' ? 'Подготовка входа через Google…' : 'Проверка аккаунта…'}</p>}
    {error && <p role="alert">{error}</p>}{notice && <p role="status">{notice}</p>}
  </section>
}
