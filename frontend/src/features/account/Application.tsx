import { Form, Link, useActionData, useLoaderData, useNavigation } from 'react-router'
import type { accountLoader, ActionResult } from '../../app/data'
import { Errors } from '../../shared/ui'
import { PendingButton } from '../../shared/Loading'
import { AccountLayout, Unfilled } from './AccountNav'
import { AnswersForm } from './AnswersForm'
import { CharacterCard } from '../games/CharacterCard'
import { useRoot } from '../../app/Shell'

const statusNames = { pending: 'подана', discussing: 'обсуждается', confirmed: 'принята', declined: 'отклонена', deleted: 'удалена' }
export function Component() {
  const { game, application, questions } = useLoaderData<typeof accountLoader>()
  const { user } = useRoot()
  const result = useActionData<ActionResult>()
  const navigation = useNavigation()
  const fields = questions.filter(question => question.order < 0)
  const unfilled = application?.answers.unfilled.filter(id => questions.some(q => q.id === id && q.order >= 0)).length || 0
  const initial = Object.fromEntries(Object.entries(application?.answers.values || {}).filter(([id]) => fields.some(q => q.id === Number(id))))
  return <AccountLayout alias={game.alias} className={!application ? 'application-empty' : ''} unfilled={unfilled}>
    <h1>Заявка {application ? statusNames[application.status] : 'не подана'}</h1>
    <Errors error={result?.error} />
    {application && application.status !== 'deleted' ? <>
      {application.character && <CharacterCard character={application.character} alias={game.alias} personal />}
      <div className="application-details">
      <p className={unfilled ? 'incomplete' : ''}>Опросник: <Link aria-label="Опросник" to={'/account/' + game.alias + '/questionnaire'}>{unfilled ? 'заполнить' : 'пройден'}</Link> <Unfilled count={unfilled} /></p>
      <p className={application.price && application.payed < application.price ? 'incomplete' : ''}>Взнос: {application.price === null ? 'не объявлен' : application.payed + ' / ' + application.price}</p>
      <h2>Дополнительная информация</h2>
      {!!fields.length && <AnswersForm key={user?.id + ':' + game.alias} alias={game.alias} questions={fields} initial={initial} />}
      <Form method="post" onSubmit={event => { if (!window.confirm('Удалить заявку?')) event.preventDefault() }}>
        <PendingButton name="intent" value="delete" pending={navigation.state !== 'idle'}>Удалить заявку</PendingButton></Form></div>
    </> : application?.status === 'deleted'
      ? <Form method="post"><PendingButton name="intent" value="restore" pending={navigation.state !== 'idle'}>Восстановить заявку</PendingButton></Form>
      : game.open_applications
        ? <Form method="post"><PendingButton name="intent" value="apply" pending={navigation.state !== 'idle'}>Подать заявку</PendingButton></Form>
        : <p>Приём заявок закрыт.</p>}
  </AccountLayout>
}
