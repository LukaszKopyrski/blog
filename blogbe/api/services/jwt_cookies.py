from typing import Optional
from django.conf import settings
from rest_framework.response import Response

class JwtCookieService:
    def _max_age(self, key: str):
        return int(settings.SIMPLE_JWT[key].total_seconds())

    def set_access(self, resp: Response, access: str):
        resp.set_cookie(
            settings.JWT_COOKIE_ACCESS_NAME,
            access,
            httponly=True,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
            path=settings.JWT_COOKIE_ACCESS_PATH,
            max_age=self._max_age("ACCESS_TOKEN_LIFETIME"),
        )

    def set_refresh(self, resp: Response, refresh: str):
        resp.set_cookie(
            settings.JWT_COOKIE_REFRESH_NAME,
            refresh,
            httponly=True,
            secure=settings.JWT_COOKIE_SECURE,
            samesite=settings.JWT_COOKIE_SAMESITE,
            path=settings.JWT_COOKIE_REFRESH_PATH,
            max_age=self._max_age("REFRESH_TOKEN_LIFETIME"),
        )

    def get_access(self, request):
        return request.COOKIES.get(settings.JWT_COOKIE_ACCESS_NAME)

    def get_refresh(self, request):
        return request.COOKIES.get(settings.JWT_COOKIE_REFRESH_NAME)

    def clear(self, resp: Response):
        resp.delete_cookie(settings.JWT_COOKIE_ACCESS_NAME, path=settings.JWT_COOKIE_ACCESS_PATH)
        resp.delete_cookie(settings.JWT_COOKIE_REFRESH_NAME, path=settings.JWT_COOKIE_REFRESH_PATH)
