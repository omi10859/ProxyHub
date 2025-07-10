from django.db import models

from apps.core.models import TimeStampedModel

class Service(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, help_text="Unique identifier used in the proxy URL")
    base_url = models.URLField(help_text="Base URL of the downstream service. Don't Include '/' in the end of url  E.g., https://httpbin.org")
    is_active = models.BooleanField(default=True)
    

class ProxyRequestLog(TimeStampedModel):

    api_key = models.CharField(max_length=128)
    downstream_service = models.CharField(max_length=255)
    path = models.TextField()
    method = models.CharField(max_length=10)
    response_status = models.IntegerField()
    duration_ms = models.FloatField()
