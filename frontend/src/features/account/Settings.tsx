import { useEffect, useState } from 'react'
import { Form, Link, useActionData, useFetcher, useLoaderData, useNavigation, useSubmit } from 'react-router'
import type { ActionResult, settingsLoader } from '../../app/data'
import { Errors } from '../../shared/ui'
import { Icon } from '../../shared/Navigation'
import { PendingButton } from '../../shared/Loading'
import { publicLink } from '../../shared/api/client'
import { AvatarEditor } from './AvatarEditor'
import type { User } from '../../shared/api/types'

export function Component() {
  const user = useLoaderData<typeof settingsLoader>()
  return <Profile key={user.id} user={user} />
}

function Profile({ user }: { user: User }) {
  const result = useActionData<ActionResult>()
  const navigation = useNavigation()
  const telegram = useFetcher<ActionResult>()
  const [expiredCode, setExpiredCode] = useState<string>()
  const [copiedCode, setCopiedCode] = useState<string>()
  const [copyError, setCopyError] = useState('')
  const link = telegram.state === 'idle' && telegram.data?.code !== expiredCode ? telegram.data : undefined
  useEffect(() => {
    const code = telegram.data?.code
    if (!code) return
    const timer = window.setTimeout(() => setExpiredCode(code), (telegram.data?.expires_in || 600) * 1000)
    return () => clearTimeout(timer)
  }, [telegram.data])
  const [avatarFile, setAvatarFile] = useState<File | null>(null)
  const submit = useSubmit()
  return <main className="settings-page"><section className="settings"><h1 className="sr-only">Настройки профиля</h1>
    <Link className="back-link" to="/account/whales/application"><Icon name="common/arrow" />Назад</Link>
    <Form method="post" encType="multipart/form-data" key={user.id} onSubmit={event => {
      event.preventDefault()
      const form = new FormData(event.currentTarget)
      if (avatarFile) form.set('avatar', avatarFile)
      void submit(form, { method: 'post', encType: 'multipart/form-data' })
    }}>
      <div className="avatar-row"><span>Аватар</span><AvatarEditor avatarUrl={user.avatar} onChange={setAvatarFile} /></div>
      <div className="form-grid">
        <label>Имя<input name="first_name" defaultValue={user.first_name} autoComplete="given-name" maxLength={100} required /></label>
        <label>Фамилия<input name="last_name" defaultValue={user.last_name} autoComplete="family-name" maxLength={100} required /></label>
        <label>Никнейм<input name="username" defaultValue={user.username} required maxLength={30} autoComplete="username" /></label>
        <label>Эл. почта<input aria-label="Email" value={user.email} readOnly type="email" /></label>
        <label>Телефон<input name="phone" type="tel" placeholder="+79000000000" defaultValue={user.phone || ''} autoComplete="tel" /></label>
        <label><span className="field-heading">Vk <small>Часть после vk.com/</small></span><input aria-label="ВКонтакте" name="vk" defaultValue={user.vk || ''} maxLength={250} /></label>
      </div>
      <fieldset><legend>Показывать в сетке ролей</legend>
        <label className="choice"><input type="checkbox" name="tg_public" aria-label="Телеграм" defaultChecked={user.tg_public} />ТГ</label>
        <label className="choice"><input type="checkbox" name="vk_public" aria-label="ВКонтакте" defaultChecked={user.vk_public} />ВК</label>
      </fieldset>
      <Errors error={result?.error} />
      {result?.saved && navigation.state === 'idle' && <p role="status">Профиль сохранён.</p>}
      <PendingButton pending={navigation.state !== 'idle'}>Сохранить профиль</PendingButton>
    </Form>
    <section className="telegram-settings"><h2>Telegram</h2><p>{user.telegram ? '@' + user.telegram : 'Не подключен'}</p>
      <telegram.Form method="post"><PendingButton name="intent" value="telegram" aria-label="Получить ссылку для подключения" pending={telegram.state !== 'idle'}>{user.telegram ? 'Переподключить Telegram' : 'Подключить Telegram'}</PendingButton></telegram.Form>
      <Errors error={telegram.data?.error} />
      {link?.url && publicLink(link.url) && <div><p>
        <a href={publicLink(link.url)} target="_blank" rel="noreferrer">Подключить Телеграм</a>
        {' '}— ссылка действует {Math.floor((link.expires_in || 600) / 60)} минут и используется один раз. Не передавайте её другим людям.</p>
        <button onClick={async () => {
          try { await navigator.clipboard.writeText(link.code!); setCopiedCode(link.code); setCopyError('') }
          catch { setCopyError('Не удалось скопировать код. Используйте ссылку для подключения.') }
        }}>{copiedCode === link.code ? 'Код скопирован' : 'Скопировать код'}</button>
        {copyError && <p role="alert">{copyError}</p>}
      </div>}
    </section>
    <Link className="button logout" aria-label="Выйти" to="/sign-out">Выход</Link>
  </section></main>
}
