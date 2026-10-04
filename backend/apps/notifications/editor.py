"""Authenticated image picker for the mailing editor."""
from io import BytesIO
from uuid import uuid4
import warnings

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, UnidentifiedImageError
from botocore.exceptions import BotoCoreError, ClientError

from config.media_storage import EditorMediaStorage


class EditorUploadForm(forms.Form):
    image = forms.FileField(label='Изображение', widget=forms.ClearableFileInput(
        attrs={'accept': 'image/jpeg,image/png,image/webp,image/gif'}))

    def clean_image(self):
        upload = self.cleaned_data['image']
        if upload.size > 5 * 1024 * 1024:
            raise ValidationError('Размер изображения не должен превышать 5 МБ.')
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(upload) as source:
                    if source.format not in {'JPEG', 'PNG', 'WEBP', 'GIF'}:
                        raise ValueError('Unsupported image format')
                    if source.width * source.height > 16_000_000:
                        raise ValueError('Image dimensions too large')
                    source.load()
                    # Re-encode raster pixels; never store active content or original metadata.
                    output = BytesIO()
                    source.convert('RGBA').save(output, format='PNG')
            return ContentFile(output.getvalue(), name=f'{uuid4().hex}.png')
        except (UnidentifiedImageError, OSError, ValueError,
                Image.DecompressionBombError, Image.DecompressionBombWarning):
            raise ValidationError('Выберите корректное изображение до 16 мегапикселей.')


def save_editor_image(image):
    storage = EditorMediaStorage() if settings.MEDIA_STORAGE == 's3' else default_storage
    try:
        name = storage.save(f'editor/{image.name}', image)
        return storage.url(name)
    except (OSError, BotoCoreError, ClientError):
        raise ValidationError('Не удалось загрузить изображение. Попробуйте ещё раз.')
