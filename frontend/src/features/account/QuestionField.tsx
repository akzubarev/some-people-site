import type { Answer, Question } from '../../shared/api/types'

export function QuestionField({ question: q, value, onChange, disabled = false }: {
  question: Question; value: Answer | undefined; onChange: (value: Answer) => void; disabled?: boolean
}) {
  const id = 'question_' + q.id
  const choices = q.choices || []
  const text = typeof value === 'string' ? value : ''
  const select = (options: string[], option: string, checked: boolean) =>
    checked ? [...options, option] : options.filter(item => item !== option)
  const description = <p id={id + '_description'} className="muted">{q.description}</p>
  if (q.type === 'line' || q.type === 'paragraph') return <div className="question">
    <div className="question-heading"><label htmlFor={id}>{q.title}{q.required && ' *'}</label>{description}</div>
    {q.type === 'line'
      ? <input id={id} name={id} placeholder="Строка..." value={text} disabled={disabled} aria-describedby={id + '_description'}
          onChange={event => onChange(event.target.value)} />
      : <textarea id={id} name={id} placeholder="Абзац..." value={text} disabled={disabled} aria-describedby={id + '_description'}
          onChange={event => onChange(event.target.value)} rows={5} />}
  </div>
  if (q.type === 'matrix' || q.type === 'matrix_checkbox') {
    const [columns = [], rows = []] = choices as string[][]
    const matrix = Array.isArray(value) ? value as string[][] : []
    return <fieldset className="question" disabled={disabled}><legend>{q.title}{q.required && ' *'}</legend>
      {description}<div className="table-scroll"><table><thead><tr><th scope="col"><span className="sr-only">Вариант</span></th>
        {columns.map(column => <th key={column} scope="col">{column}</th>)}</tr></thead>
        <tbody>{rows.map((row, index) => <tr key={row}><th scope="row">{row}</th>
          {columns.map(column => <td key={column}><input type={q.type === 'matrix' ? 'radio' : 'checkbox'}
            aria-label={row + ': ' + column} name={id + '_' + index}
            checked={(matrix[index] || []).includes(column)}
            onChange={event => onChange(rows.map((_, i) => i === index
              ? q.type === 'matrix' ? [column] : select(matrix[index] || [], column, event.target.checked)
              : matrix[i] || []))} /></td>)}</tr>)}</tbody></table></div>
    </fieldset>
  }
  return <fieldset className="question" disabled={disabled}>
    <legend>{q.title}{q.required && ' *'}</legend>{description}
    {q.type === 'scale' && <div className="scale-progress" aria-hidden="true"><div style={{ width: Math.max(0, (choices as string[]).indexOf(text)) / Math.max(1, choices.length - 1) * 100 + '%' }} /></div>}
    <div className={q.type === 'scale' ? 'scale' : 'choices'}>{(choices as string[]).map(option =>
      <label className="choice" key={option}><input name={id} type={q.type === 'multiple_choice' ? 'checkbox' : 'radio'}
        checked={q.type === 'multiple_choice' ? Array.isArray(value) && (value as string[]).includes(option) : value === option}
        onChange={event => onChange(q.type === 'multiple_choice'
          ? select(Array.isArray(value) ? value as string[] : [], option, event.target.checked) : option)} />{option}</label>)}</div>
  </fieldset>
}
