import traceback


def readable_exception(e: Exception, verbose=False):
    """
    Вспомогательная функция для вывода исключений для удобства отладки
    """
    message = None
    if verbose is True:
        message = traceback.format_exc()
    if message is None:
        message = str(e)
    return f"{message}| Handled"
