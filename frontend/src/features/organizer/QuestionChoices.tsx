import { useState } from 'react'
import { QuestionField } from '../account/QuestionField'
import type { Answer, Question } from '../../shared/api/types'

export function QuestionChoices({ type, choices, change, disabled, title }: {
  type: string; choices: unknown; change: (value: string[] | string[][]) => void; disabled: boolean; title: string
}) {
  const [answer, setAnswer] = useState<Answer>('')
  const matrix = type === 'matrix' || type === 'matrix_checkbox'
  const values = Array.isArray(choices) ? choices : []
  const columns: string[] = matrix ? (Array.isArray(values[0]) ? values[0] : []) : values.filter(v => typeof v === 'string')
  const rows: string[] = matrix && Array.isArray(values[1]) ? values[1] : []
  function update(next: string[], axis: 'columns' | 'rows') { change(matrix ? axis === 'columns' ? [next, rows] : [columns, next] : next) }
  function controls(items: string[], index: number, axis: 'columns' | 'rows') {
    const move = (offset: number) => { const next = [...items]; [next[index], next[index + offset]] = [next[index + offset], next[index]]; update(next, axis) }
    return <div className="organizer-choice-actions"><button type="button" disabled={disabled || index === 0} onClick={() => move(-1)} aria-label="Передвинуть назад">←</button>
      <button type="button" disabled={disabled || index === items.length - 1} onClick={() => move(1)} aria-label="Передвинуть вперёд">→</button>
      <button type="button" disabled={disabled} onClick={() => update(items.filter((_, i) => i !== index), axis)}>Удалить</button></div>
  }
  const option = (items: string[], index: number, axis: 'columns' | 'rows') => <>
    <input aria-label={`${axis === 'rows' ? 'Строка' : 'Вариант'} ${index + 1}`} value={items[index]} disabled={disabled} maxLength={500}
      onChange={event => update(items.map((v, i) => i === index ? event.target.value : v), axis)} />{controls(items, index, axis)}</>
  if (type === 'line' || type === 'paragraph') return null
  return <div className="organizer-full organizer-choice-editor">
    {disabled && <p>Варианты защищены, поскольку на вопрос уже ответили.</p>}
    {matrix ? <div className="table-scroll"><table><thead><tr><th>Строки / столбцы</th>{columns.map((_, i) => <th key={i}>{option(columns, i, 'columns')}</th>)}</tr></thead>
      <tbody>{rows.map((_, i) => <tr key={i}><th>{option(rows, i, 'rows')}</th>{columns.map((column, j) => <td key={j}>
        <input type={type === 'matrix' ? 'radio' : 'checkbox'} name={'matrix-preview-' + i} aria-label={`${rows[i]}: ${column}`} /></td>)}</tr>)}</tbody></table></div>
      : <div className={type === 'scale' ? 'organizer-scale-editor' : 'organizer-option-editor'}>{columns.map((_, i) => <div key={i}>{option(columns, i, 'columns')}</div>)}</div>}
    <div className="organizer-actions"><button type="button" disabled={disabled} onClick={() => update([...columns, ''], 'columns')}>
      {matrix ? 'Добавить столбец' : type === 'scale' ? 'Добавить деление' : 'Добавить вариант'}</button>
      {matrix && <button type="button" disabled={disabled} onClick={() => update([...rows, ''], 'rows')}>Добавить строку</button>}</div>
    <details><summary>Предпросмотр для игрока</summary><QuestionField question={{ id: -1, title, description: '', required: false,
      type, choices: matrix ? [columns, rows] : columns, order: 1 } as Question} value={answer} onChange={setAnswer} /></details>
  </div>
}
