import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model, swapped in from day one via AUTH_USER_MODEL.

    This has to happen in Module 1: Django makes it very painful to switch
    AUTH_USER_MODEL after the first migration has run. Fields for
    registration/login flows (Module 2) build on top of this.

    UUID primary key to match the global 'IDs: UUID' convention -- an
    incrementing integer user id would let anyone estimate total signups
    just by creating an account and looking at their own id.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
