import { useEffect, useRef, useState } from 'react'
import { Picture } from '../../shared/ui'
import { avatar } from '../../shared/assets'
import { Icon } from '../../shared/Navigation'

export function AvatarEditor({ onChange, avatarUrl }: { onChange: (file: File | null) => void; avatarUrl?: string | null }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [source, setSource] = useState<File | null>(null)
  const [picture, setPicture] = useState<HTMLImageElement | null>(null)
  const [zoom, setZoom] = useState(1)
  const [x, setX] = useState(50)
  const [y, setY] = useState(50)
  const [error, setError] = useState('')
  useEffect(() => {
    if (!source) return
    const url = URL.createObjectURL(source)
    const image = new Image()
    let cancelled = false
    image.onload = () => { if (!cancelled) setPicture(image) }
    image.onerror = () => { if (!cancelled) setError('Не удалось открыть изображение.') }
    image.src = url
    return () => { cancelled = true; URL.revokeObjectURL(url) }
  }, [source])
  useEffect(() => {
    const context = canvas.current?.getContext('2d')
    if (!picture || !context) return
    const side = Math.min(picture.naturalWidth, picture.naturalHeight) / zoom
    context.drawImage(picture, (picture.naturalWidth - side) * x / 100,
      (picture.naturalHeight - side) * y / 100, side, side, 0, 0, 512, 512)
    let cancelled = false
    canvas.current!.toBlob(blob => {
      if (!cancelled && blob) onChange(new File([blob], 'avatar.png', { type: 'image/png' }))
    }, 'image/png')
    return () => { cancelled = true }
  }, [picture, zoom, x, y, onChange])
  return <section className="avatar-editor">
    <label className={!avatarUrl ? 'avatar-empty' : ''}><span className="sr-only">Аватар</span><Picture src={avatarUrl} fallback={avatar} alt="Ваш аватар" className="profile-avatar" />
      <span className="camera-icon"><Icon name="image-uploader/camera" /></span><input type="file" accept="image/png,image/jpeg,image/webp"
      onChange={event => {
        const file = event.target.files?.[0]
        onChange(null)
        setPicture(null)
        setSource(null)
        if (!file) return
        if (file.size > 5 * 1024 * 1024 || !['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) {
          setError('Выберите PNG, JPEG или WebP размером до 5 МБ.')
          event.target.value = ''
          return
        }
        setError('')
        setZoom(1); setX(50); setY(50); setSource(file)
      }} /></label>
    {error && <p role="alert">{error}</p>}
    {picture && <div className="crop-controls">
      <canvas ref={canvas} width={512} height={512} aria-label="Предпросмотр аватара" />
      <label>Масштаб<input type="range" min="1" max="3" step=".05" value={zoom} onChange={event => setZoom(Number(event.target.value))} /></label>
      <label>По горизонтали<input type="range" min="0" max="100" value={x} onChange={event => setX(Number(event.target.value))} /></label>
      <label>По вертикали<input type="range" min="0" max="100" value={y} onChange={event => setY(Number(event.target.value))} /></label>
    </div>}
  </section>
}
