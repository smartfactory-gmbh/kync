from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.middleware.common import MiddlewareMixin
from django_cprofile_middleware.middleware import (
    ProfilerMiddleware as BaseProfilerMiddleware,
)


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "X-HealthCheck" in request.headers:
            return HttpResponse("OK", content_type="text/plain")
        return self.get_response(request)


class IPMiddleware(MiddlewareMixin):
    def __call__(self, request: HttpRequest):
        if settings.USE_X_FORWARDED_HOST and "HTTP_X_FORWARDED_FOR" in request.META:
            request.META["X-IP"] = request.META.get("HTTP_X_FORWARDED_FOR").split(",").pop(0).strip()
        else:
            request.META["X-IP"] = request.META.get("REMOTE_ADDR")
        return self.get_response(request)


class ProfilerMiddleware(BaseProfilerMiddleware):
    def can(self, request):
        # We want to enable the possibility to profile even on test, stage and prod systems
        # - There is no performance impact for requests without the 'prof' GET parameter
        # - There is no security issue as only staff users can trigger the profiler
        requires_staff = getattr(settings, "DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF", True)

        if requires_staff and not (request.user and request.user.is_staff):
            return False

        return "prof" in request.GET
