(() => {
  const result = document.getElementById('upload-result');
  if (!result) return;
  const { callback, url } = JSON.parse(result.textContent);
  try {
    // Prose Editor implements this established picker protocol itself.
    // No CKEditor library is loaded or required.
    if (window.opener && window.opener.location.origin === window.location.origin
        && window.opener.CKEDITOR?.tools?.callFunction) {
      window.opener.CKEDITOR.tools.callFunction(callback, url);
      window.close();
      return;
    }
  } catch { /* A closed or cross-origin opener leaves a copyable URL. */ }
  document.getElementById('upload-status').textContent =
    'Скопируйте ссылку в поле адреса изображения в редакторе.';
})();
