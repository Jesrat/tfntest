import pytz
from django.conf import settings
from django.utils import timezone, translation


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous:
            # noinspection PyBroadException
            try:
                timezone.activate(pytz.timezone(request.user.timezone))
            except Exception:
                pass
        return self.get_response(request)


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous and request.user.is_authenticated:
            # noinspection PyBroadException
            try:
                translation.activate(request.user.language)
                response = self.get_response(request)
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.user.language)
                return response
            except Exception:
                pass
        return self.get_response(request)
