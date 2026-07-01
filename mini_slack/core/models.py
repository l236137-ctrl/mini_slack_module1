import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base for domain models. Gives every table a UUID primary key
    (per the global 'IDs: UUID, not auto-increment' convention) plus
    created_at/updated_at timestamps, so later modules don't repeat this.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
