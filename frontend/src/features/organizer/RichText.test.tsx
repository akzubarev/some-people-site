import { cleanup, render, screen, waitFor } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import { RichText } from './RichText'

afterEach(cleanup)
it('preserves existing HTML and does not report edits when busy or read-only state changes', async () => {
  const change = vi.fn()
  const value = '<p><strong>Saved message</strong></p><table><tbody><tr><td><p>Cell</p></td></tr></tbody></table><img src="/api/media/editor/synthetic/" alt="Portrait">'
  const props = { value, change, uploadEndpoint: 'organizer/games/1/mailings/upload/' }
  const { rerender } = render(<RichText {...props} disabled={false} />)
  const editor = await screen.findByRole('textbox', { name: 'Текст рассылки' })
  await waitFor(() => expect(editor.querySelector('strong')?.textContent).toBe('Saved message'))
  expect(editor.querySelector('table')?.textContent).toBe('Cell')
  expect(editor.querySelector('img')?.getAttribute('src')).toBe('/api/media/editor/synthetic/')
  rerender(<RichText {...props} disabled />)
  await waitFor(() => expect(editor.getAttribute('contenteditable')).toBe('false'))
  rerender(<RichText {...props} disabled={false} />)
  await waitFor(() => expect(editor.getAttribute('contenteditable')).toBe('true'))
  expect(change).not.toHaveBeenCalled()
})
