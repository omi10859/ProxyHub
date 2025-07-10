import uuid

from django.db import models
from apps.core.models import TimeStampedModel

class ClientKey(TimeStampedModel):

    key = models.UUIDField(default=uuid.uuid4)

    name = models.CharField(max_length=255)
