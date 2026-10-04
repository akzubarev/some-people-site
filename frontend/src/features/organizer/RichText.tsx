import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import { TableKit } from '@tiptap/extension-table'
import { useEffect, useState } from 'react'
import { api } from '../../shared/api/client'

export function RichText({ value, change, disabled, uploadEndpoint }: { value: string; change: (html: string) => void; disabled: boolean; uploadEndpoint: string }) {
  const [link, setLink] = useState(''), [uploading, setUploading] = useState(false), [error, setError] = useState('')
  const editor = useEditor({ immediatelyRender: false, extensions: [StarterKit, Image, TableKit], content: value, editable: !disabled,
    onUpdate: ({ editor }) => change(editor.getHTML()), editorProps: { attributes: { 'aria-label': 'Текст рассылки', role: 'textbox' } } })
  useEffect(() => { if (editor && !editor.isDestroyed) editor.setEditable(!disabled, false) }, [editor, disabled])
  useEffect(() => { if (editor && !editor.isDestroyed && editor.getHTML() !== value) editor.commands.setContent(value, { emitUpdate: false }) }, [editor, value])
  if (!editor || editor.isDestroyed) return <p>Загрузка редактора…</p>
  return <div className="organizer-rich-text"><div className="organizer-actions" role="toolbar" aria-label="Форматирование текста">
    <button type="button" disabled={disabled} aria-pressed={editor.isActive('bold')} onClick={() => editor.chain().focus().toggleBold().run()}>Жирный</button>
    <button type="button" disabled={disabled} aria-pressed={editor.isActive('italic')} onClick={() => editor.chain().focus().toggleItalic().run()}>Курсив</button>
    <button type="button" disabled={disabled} onClick={() => editor.chain().focus().toggleBulletList().run()}>Список</button>
    <button type="button" disabled={disabled} onClick={() => editor.chain().focus().toggleOrderedList().run()}>Нумерация</button>
    <button type="button" disabled={disabled} onClick={() => editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()}>Таблица</button>
    <button type="button" disabled={disabled || !editor.can().undo()} onClick={() => editor.chain().focus().undo().run()}>Отменить</button>
    <button type="button" disabled={disabled || !editor.can().redo()} onClick={() => editor.chain().focus().redo().run()}>Повторить</button>
    {editor.isActive('table') && <><button type="button" disabled={disabled} onClick={() => editor.chain().focus().addRowAfter().run()}>Добавить строку</button>
      <button type="button" disabled={disabled} onClick={() => editor.chain().focus().addColumnAfter().run()}>Добавить столбец</button>
      <button type="button" disabled={disabled} onClick={() => editor.chain().focus().deleteRow().run()}>Удалить строку</button>
      <button type="button" disabled={disabled} onClick={() => editor.chain().focus().deleteColumn().run()}>Удалить столбец</button>
      <button type="button" disabled={disabled} onClick={() => editor.chain().focus().deleteTable().run()}>Удалить таблицу</button></>}
  </div><div className="organizer-rich-tools"><label>Адрес ссылки<input type="url" value={link} disabled={disabled} onChange={e => setLink(e.target.value)} /></label>
    <button type="button" disabled={disabled || !/^https?:\/\//i.test(link)} onClick={() => editor.chain().focus().extendMarkRange('link').setLink({ href: link }).run()}>Вставить ссылку</button>
    <button type="button" disabled={disabled} onClick={() => editor.chain().focus().unsetLink().run()}>Убрать ссылку</button>
    <label>{uploading ? 'Загружаем изображение…' : 'Изображение (до 5 МБ)'}<input type="file" disabled={disabled || uploading} accept="image/png,image/jpeg,image/webp,image/gif" onChange={async e => {
      const file = e.target.files?.[0]; if (!file) return
      e.target.value = ''; setError('')
      if (file.size > 5 * 1024 * 1024) { setError('Максимальный размер — 5 МБ.'); return }
      setUploading(true)
      try { const form = new FormData(); form.set('image', file); const result = await api<{ url: string }>(uploadEndpoint, { method: 'POST', body: form }); editor.chain().focus().setImage({ src: result.url, alt: file.name }).run() }
      catch { setError('Не удалось загрузить изображение. Попробуйте ещё раз.') } finally { setUploading(false) }
    }} /></label></div>{error && <p role="alert">{error}</p>}<EditorContent editor={editor} />
    <p className="organizer-note">В Telegram таблицы становятся текстом, изображения — ссылками. Поддерживаемое форматирование сохраняется.</p></div>
}
