import uuid

from django.http import JsonResponse
from apps.client.models import ClientKey    

class APIKeyRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return JsonResponse({'detail': 'Missing API key'}, status=401)
        try:
            key = uuid.UUID(api_key)
        except Exception:
            return JsonResponse({'detail': 'Invalid API key'}, status=401)
        if not ClientKey.objects.filter(key=key).exists():
            return JsonResponse({'detail': 'Invalid API key'}, status=401)
        return super().dispatch(request, *args, **kwargs)
