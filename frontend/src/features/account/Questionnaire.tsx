import { Link, useLoaderData } from 'react-router'
import type { accountLoader } from '../../app/data'
import { AccountLayout } from './AccountNav'
import { AnswersForm } from './AnswersForm'
import { useRoot } from '../../app/Shell'

export function Component() {
  const { game, application, questions } = useLoaderData<typeof accountLoader>()
  const { user } = useRoot()
  const fields = questions.filter(question => question.order >= 0)
  const initial = Object.fromEntries(Object.entries(application?.answers.values || {}).filter(([id]) => fields.some(q => q.id === Number(id))))
  return <AccountLayout alias={game.alias} className="questionnaire" unfilled={application?.answers.unfilled.filter(id => fields.some(q => q.id === id)).length || 0}>
    <h1>Персонажный опросник</h1>
    {application && application.status !== 'deleted' ? <>
      <p className="preserve">{'Отметь “Хочу” - если предпочитаешь опцию, “Ок” - если не против, “Не хочу” - если она тебе не нравится, но в целом ты к ней готов, “Строго нет” - если точно не готов играть таких персонажей.\nДля лучших результатов давай разнообразные ответы, не выбирай одни “хочу” или одни “не хочу”.\n\nЕсли тебе понравились конкретные персонажи, лайкни их в сетке ролей, и мы это увидим'}</p>
      {fields.length ? <AnswersForm key={user?.id + ':' + game.alias} alias={game.alias} questions={fields} initial={initial} />
        : <p>Вопросов пока нет.</p>}
    </> : <p>Сначала <Link to={'/account/' + game.alias + '/application'}>подайте или восстановите заявку</Link>.</p>}
  </AccountLayout>
}
