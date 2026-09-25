import { useEffect, useRef, useState } from 'react'
import { Picture } from '../../shared/ui'
import { avatar } from '../../shared/assets'

function SelectedAvatar({ file }: { file: File }) {
  const ref = useRef<HTMLImageElement>(null)
  useEffect(() => {
    const url = URL.createObjectURL(file)
    ref.current!.src = url
    return () => URL.revokeObjectURL(url)
  }, [file])
  return <img ref={ref} alt="Ваш аватар" className="profile-avatar" />
}

function CropDialog({ picture, onApply, onClose }: {
  picture: HTMLImageElement; onApply: (file: File) => void; onClose: () => void
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const canvas = useRef<HTMLCanvasElement>(null)
  const active = useRef(true)
  const drag = useRef<{ x: number; y: number; cropX: number; cropY: number } | null>(null)
  const [zoom, setZoom] = useState(1)
  const [x, setX] = useState(50)
  const [y, setY] = useState(50)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const side = Math.min(picture.naturalWidth, picture.naturalHeight) / zoom
  useEffect(() => {
    active.current = true
    const element = dialog.current!
    element.showModal()
    return () => { active.current = false; element.close() }
  }, [])
  useEffect(() => {
    const context = canvas.current!.getContext('2d')!
    context.clearRect(0, 0, 512, 512)
    context.drawImage(picture, (picture.naturalWidth - side) * x / 100,
      (picture.naturalHeight - side) * y / 100, side, side, 0, 0, 512, 512)
  }, [picture, side, x, y])
  return <dialog ref={dialog} className="avatar-dialog" aria-labelledby="avatar-dialog-title" onCancel={onClose}>
    <h2 id="avatar-dialog-title">Выберите область фото</h2>
    <p>Перетащите фото и настройте масштаб.</p>
    <canvas ref={canvas} width={512} height={512} aria-label="Предпросмотр аватара"
      onPointerDown={event => {
        event.currentTarget.setPointerCapture(event.pointerId)
        drag.current = { x: event.clientX, y: event.clientY, cropX: x, cropY: y }
      }} onPointerMove={event => {
        if (!drag.current) return
        const scale = side / event.currentTarget.getBoundingClientRect().width
        const clamp = (value: number) => Math.max(0, Math.min(100, value))
        if (picture.naturalWidth > side)
          setX(clamp(drag.current.cropX - (event.clientX - drag.current.x) * scale / (picture.naturalWidth - side) * 100))
        if (picture.naturalHeight > side)
          setY(clamp(drag.current.cropY - (event.clientY - drag.current.y) * scale / (picture.naturalHeight - side) * 100))
      }} onPointerUp={() => { drag.current = null }} onPointerCancel={() => { drag.current = null }} />
    <label>Масштаб<input type="range" min="1" max="3" step=".05" value={zoom} onChange={event => setZoom(Number(event.target.value))} /></label>
    <details className="avatar-position"><summary>Точное положение</summary>
      <label>По горизонтали<input type="range" min="0" max="100" value={x} onChange={event => setX(Number(event.target.value))} /></label>
      <label>По вертикали<input type="range" min="0" max="100" value={y} onChange={event => setY(Number(event.target.value))} /></label>
    </details>
    {error && <p role="alert">{error}</p>}
    <div className="profile-actions"><button type="button" className="profile-button profile-button--secondary" onClick={onClose}>Отмена</button>
      <button type="button" className="profile-button" disabled={saving} onClick={() => {
        setSaving(true)
        canvas.current!.toBlob(blob => {
          if (!active.current) return
          if (blob) { onApply(new File([blob], 'avatar.png', { type: 'image/png' })); onClose() }
          else { setSaving(false); setError('Не удалось подготовить фото. Попробуйте другое изображение.') }
        }, 'image/png')
      }}>{saving ? 'Подготовка…' : 'Применить фото'}</button></div>
  </dialog>
}

export function AvatarEditor({ onChange, avatarUrl, value }: {
  onChange: (file: File | null) => void; avatarUrl?: string | null; value: File | null
}) {
  const input = useRef<HTMLInputElement>(null)
  const [source, setSource] = useState<File | null>(null)
  const [picture, setPicture] = useState<HTMLImageElement | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  useEffect(() => {
    if (!source) return
    const url = URL.createObjectURL(source)
    const image = new Image()
    let cancelled = false
    image.onload = () => { if (!cancelled) { setPicture(image); setLoading(false) } }
    image.onerror = () => { if (!cancelled) { setError('Не удалось открыть изображение.'); setLoading(false) } }
    image.src = url
    return () => { cancelled = true; URL.revokeObjectURL(url) }
  }, [source])
  return <section className="avatar-editor" aria-label="Фото профиля">
    {value ? <SelectedAvatar file={value} />
      : <Picture src={avatarUrl} fallback={avatar} alt="Ваш аватар" className="profile-avatar" />}
    <div className="avatar-editor-actions"><h2>Аватар</h2>
      <p>PNG, JPEG или WebP, до 5 МБ.</p>
      <input ref={input} className="sr-only" aria-label="Аватар" tabIndex={-1} type="file" accept="image/png,image/jpeg,image/webp"
        onChange={event => {
          const file = event.target.files?.[0]
          event.target.value = ''
          if (!file) return
          if (file.size > 5 * 1024 * 1024 || !['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) {
            setError('Выберите PNG, JPEG или WebP размером до 5 МБ.'); return
          }
          setError(''); setLoading(true); setSource(file)
        }} />
      <button type="button" className="profile-button profile-button--secondary" disabled={loading} onClick={() => input.current!.click()}>{loading ? 'Открываем фото…' : 'Выбрать фото'}</button>
      {value && <p className="avatar-unsaved">Новое фото будет загружено при сохранении профиля.</p>}
      {error && <p role="alert" className="error">{error}</p>}
    </div>
    {picture && <CropDialog picture={picture} onApply={onChange} onClose={() => { setPicture(null); setSource(null) }} />}
  </section>
}
