import uuid

from django.db import models

class ClientKey(models.Model):

    key = models.UUIDField(default=uuid.uuid4)

    name = models.CharField(max_length=255)