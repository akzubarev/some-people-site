from django.conf import settings
from django.utils import translation


def LocaleMiddleware(get_response):
    def middleware(request):
        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES.keys():
            # print(request.COOKIES[settings.LANGUAGE_COOKIE_NAME])
            # translation.activate(request.COOKIES[settings.LANGUAGE_COOKIE_NAME])
            translation.activate('{lang}-{lang}'.format(
                lang=request.COOKIES[settings.LANGUAGE_COOKIE_NAME]))
            # print('tetst')
        # print(request.COOKIES[settings.LANGUAGE_COOKIE_NAME])
        # translation.activate('en')
        # print(translation.get_language())
        response = get_response(request)
        return response

    return middleware
