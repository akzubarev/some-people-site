import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import { QuestionField } from './QuestionField'
import type { Question } from '../../shared/api/types'
afterEach(cleanup)
const base: Question = { id: 1, title: 'Question', description: '', type: 'line', choices: null, required: true, order: 1 }
it('keeps matrix radio answers separate by row', () => {
  const change = vi.fn()
  render(<QuestionField question={{ ...base, type: 'matrix', choices: [['A', 'B'], ['One', 'Two']] }}
    value={ [['A'], ['B']] } onChange={change} />)
  fireEvent.click(screen.getByLabelText('One: B'))
  expect(change).toHaveBeenCalledWith([['B'], ['B']])
})
it('can clear a checkbox answer and a text answer', () => {
  const change = vi.fn()
  const { rerender } = render(<QuestionField question={{ ...base, type: 'multiple_choice', choices: ['A', 'B'] }}
    value={['A']} onChange={change} />)
  fireEvent.click(screen.getByLabelText('A'))
  expect(change).toHaveBeenCalledWith([])
  rerender(<QuestionField question={base} value="old" onChange={change} />)
  fireEvent.change(screen.getByLabelText('Question *'), { target: { value: '' } })
  expect(change).toHaveBeenLastCalledWith('')
})
it('does not let read-only answers change', () => {
  const change = vi.fn()
  render(<QuestionField disabled question={{ ...base, type: 'single_choice', choices: ['A'] }}
    value="A" onChange={change} />)
  expect((screen.getByLabelText('A') as HTMLInputElement).closest('fieldset')?.disabled).toBe(true)
})
