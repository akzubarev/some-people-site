import { useEffect, useRef, useState } from 'react'
import { useBeforeUnload, useBlocker } from 'react-router'
import type { Answer, Question } from '../../shared/api/types'
import { ApiError, json } from '../../shared/api/client'
import { Errors } from '../../shared/ui'
import { Spinner } from '../../shared/Loading'
import { QuestionField } from './QuestionField'

/** Serialize saves so an older response can never overwrite a newer edit. */
export function AnswersForm({ alias, questions, initial }: {
  alias: string; questions: Question[]; initial: Record<string, Answer>
}) {
  const [answers, setAnswers] = useState(initial)
  const [saved, setSaved] = useState(JSON.stringify(initial))
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<Record<string, unknown>>()
  const [retry, setRetry] = useState(0)
  const chain = useRef(Promise.resolve())
  const snapshot = JSON.stringify(answers)
  const dirty = snapshot !== saved
  const blocker = useBlocker(dirty)
  useBeforeUnload(event => { if (dirty) { event.preventDefault(); event.returnValue = '' } })
  useEffect(() => {
    if (!dirty) return
    let cancelled = false
    const timer = window.setTimeout(() => {
      chain.current = chain.current.then(async () => {
        if (cancelled) return
        setSaving(true)
        setError(undefined)
        try {
          const values = JSON.parse(snapshot) as Record<string, Answer>
          await json('applications/apply/', { game_alias: alias,
            ...Object.fromEntries(Object.entries(values).map(([id, value]) => ['question_' + id, value])) })
          if (!cancelled) setSaved(snapshot)
        } catch (failure) {
          if (!cancelled) setError(failure instanceof ApiError ? failure.fields
            : { detail: 'Ответы не сохранены. Проверьте соединение и повторите.' })
        } finally { if (!cancelled) setSaving(false) }
      })
    }, 800)
    return () => { cancelled = true; clearTimeout(timer) }
  }, [alias, snapshot, dirty, retry])
  return <div>
    {questions.map(question => <QuestionField key={question.id} question={question} value={answers[question.id]}
      onChange={value => setAnswers(current => ({ ...current, [question.id]: value }))} />)}
    <p role="status" className="loading-message">{saving && <Spinner />}
      {saving ? 'Сохраняем…' : dirty ? 'Есть несохранённые изменения.' : 'Все изменения сохранены.'}</p>
    <Errors error={error} />
    {error && <button onClick={() => setRetry(count => count + 1)}>Повторить сохранение</button>}
    {blocker.state === 'blocked' && <div role="alertdialog" aria-modal="true" aria-label="Несохранённые ответы" className="modal-backdrop">
      <div className="panel"><h2>Есть несохранённые ответы</h2><p>Дождитесь сохранения или останьтесь на странице.</p>
        <button onClick={() => blocker.reset()}>Остаться</button>
        {!saving && <button onClick={() => blocker.proceed()}>Уйти без сохранения</button>}
      </div></div>}
  </div>
}
