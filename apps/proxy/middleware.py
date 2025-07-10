import time
from django.http import JsonResponse
from django.core.cache import cache

class RateLimitMixin:
    RATE_LIMIT = 100
    PERIOD = 3600
    API_KEY_HEADER = "X-API-KEY"

    def get_cache_key(self, request):
        api_key = request.headers.get(self.API_KEY_HEADER)
        if not api_key:
            return None
        window_start = int(time.time() // self.PERIOD)
        return f"rl:{api_key}:{window_start}"

    def dispatch(self, request, *args, **kwargs):
        cache_key = self.get_cache_key(request)
        if cache_key is None:
            return super().dispatch(request, *args, **kwargs)
        try:
            count = cache.incr(cache_key)
            if count == 1:
                cache.expire(cache_key, self.PERIOD)
        except ValueError:
            cache.set(cache_key, 1, timeout=self.PERIOD)
            count = 1

        if count > self.RATE_LIMIT:
            return JsonResponse(
                {"detail": f"Request limit of {self.RATE_LIMIT} per hour exceeded."},
                status=429,
            )

        response = super().dispatch(request, *args, **kwargs)
        return response