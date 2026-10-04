"""Authenticated image picker for the mailing editor."""
from io import BytesIO
from uuid import uuid4
import warnings

from django import forms
from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from PIL import Image, UnidentifiedImageError
from botocore.exceptions import BotoCoreError, ClientError

from config.media_storage import EditorMediaStorage


class EditorUploadForm(forms.Form):
    image = forms.FileField(label='Изображение', widget=forms.ClearableFileInput(
        attrs={'accept': 'image/jpeg,image/png,image/webp,image/gif'}))
    callback = forms.IntegerField(min_value=0, max_value=2147483647,
                                  widget=forms.HiddenInput)

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


@require_http_methods(['GET', 'POST'])
@csrf_protect
@never_cache
def editor_upload(request):
    user = request.user
    if not (user.is_authenticated and user.is_active
            and (user.is_staff or user.is_superuser)
            and (user.has_perm('notifications.add_mailing')
                 or user.has_perm('notifications.change_mailing'))):
        raise PermissionDenied
    form = EditorUploadForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        initial={'callback': request.GET.get('CKEditorFuncNum', '')},
    )
    result = None
    if request.method == 'POST' and form.is_valid():
        storage = EditorMediaStorage() if settings.MEDIA_STORAGE == 's3' else default_storage
        image = form.cleaned_data['image']
        try:
            name = storage.save(f'editor/{image.name}', image)
            result = {'callback': form.cleaned_data['callback'], 'url': storage.url(name)}
        except (OSError, BotoCoreError, ClientError):
            form.add_error(None, 'Не удалось загрузить изображение. Попробуйте ещё раз.')
    return render(request, 'notifications/editor_upload.html', {'form': form, 'result': result})
