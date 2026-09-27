import { useEffect, useState } from 'react'
import { Form, useActionData, useFetcher, useLoaderData, useNavigation, useSearchParams, useSubmit } from 'react-router'
import type { ActionResult, settingsLoader } from '../../app/data'
import { Errors } from '../../shared/ui'
import { PendingButton } from '../../shared/Loading'
import { publicLink } from '../../shared/api/client'
import { AvatarEditor } from './AvatarEditor'
import type { User } from '../../shared/api/types'
import { AccountLayout } from './AccountNav'
import { useRoot } from '../../app/Shell'

export function Component() {
  const user = useLoaderData<typeof settingsLoader>()
  return <Profile key={user.id} user={user} />
}

function Profile({ user }: { user: User }) {
  const { games } = useRoot()
  const [params] = useSearchParams()
  const alias = games.find(game => game.alias === params.get('game'))?.alias
    || games.find(game => game.alias === 'whales')?.alias || games[0]?.alias || 'whales'
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
  const [previousResult, setPreviousResult] = useState(result)
  if (previousResult !== result) {
    setPreviousResult(result)
    if (result?.saved) setAvatarFile(null)
  }
  const submit = useSubmit()
  return <AccountLayout alias={alias} className="profile-settings"><h1>Настройки профиля</h1>
    <Form method="post" encType="multipart/form-data" key={user.id} onSubmit={event => {
      event.preventDefault()
      const form = new FormData(event.currentTarget)
      if (avatarFile) form.set('avatar', avatarFile)
      void submit(form, { method: 'post', encType: 'multipart/form-data' })
    }}>
      <AvatarEditor avatarUrl={user.avatar} value={avatarFile} onChange={setAvatarFile} />
      <fieldset className="profile-section"><legend>Личные данные</legend><div className="form-grid">
        <label>Имя<input name="first_name" defaultValue={user.first_name} autoComplete="given-name" maxLength={100} required /></label>
        <label>Фамилия<input name="last_name" defaultValue={user.last_name} autoComplete="family-name" maxLength={100} required /></label>
        <label>Никнейм<input name="username" defaultValue={user.username} required maxLength={30} autoComplete="username" /></label>
        <label>Эл. почта<input aria-label="Email" value={user.email} readOnly type="email" /></label>
        <label>Телефон<input name="phone" type="tel" placeholder="+79000000000" defaultValue={user.phone || ''} autoComplete="tel" /></label>
        <label>ВКонтакте<input name="vk" defaultValue={user.vk || ''} placeholder="vk.com/username" maxLength={250} /></label>
      </div></fieldset>
      <fieldset className="profile-visibility"><legend>Показывать в сетке ролей</legend><div>
        <label className="choice"><input type="checkbox" name="tg_public" aria-label="Телеграм" defaultChecked={user.tg_public} />ТГ</label>
        <label className="choice"><input type="checkbox" name="vk_public" aria-label="ВКонтакте" defaultChecked={user.vk_public} />ВК</label>
      </div></fieldset>
      <Errors error={result?.error} />
      {result?.saved && navigation.state === 'idle' && <p role="status">Профиль сохранён.</p>}
      <div className="profile-actions"><PendingButton className="profile-button" pending={navigation.state !== 'idle'}>Сохранить профиль</PendingButton></div>
    </Form>
    <section className="telegram-settings"><h2>Telegram</h2><p>{user.telegram ? 'Подключён: @' + user.telegram : 'Подключите Telegram, чтобы получать сообщения об игре.'}</p>
      <telegram.Form method="post"><input type="hidden" name="intent" value="telegram" /><PendingButton className="profile-button profile-button--secondary" aria-label="Получить ссылку для подключения" pending={telegram.state !== 'idle'}>{user.telegram ? 'Обновить подключение' : 'Получить ссылку'}</PendingButton></telegram.Form>
      <Errors error={telegram.data?.error} />
      {link?.url && publicLink(link.url) && <div className="telegram-link-result">
        <label>Ссылка для подключения<input readOnly value={link.url} onFocus={event => event.currentTarget.select()} /></label>
        <p>Откройте ссылку и нажмите «Старт» в боте. Ссылка действует {Math.floor((link.expires_in || 600) / 60)} минут и используется один раз.</p>
        <div className="profile-actions"><a className="profile-button" href={publicLink(link.url)} target="_blank" rel="noreferrer">Открыть Telegram</a>
        <button type="button" className="profile-button profile-button--secondary" onClick={async () => {
          try { await navigator.clipboard.writeText(link.url!); setCopiedCode(link.code); setCopyError('') }
          catch { setCopyError('Не удалось скопировать ссылку. Выделите её в поле выше и скопируйте вручную.') }
        }}>{copiedCode === link.code ? 'Ссылка скопирована' : 'Скопировать ссылку'}</button></div>
        {copyError && <p role="alert">{copyError}</p>}
      </div>}
      {expiredCode && expiredCode === telegram.data?.code && <p role="status">Срок ссылки истёк. Получите новую ссылку.</p>}
    </section>
  </AccountLayout>
}
