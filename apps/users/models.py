
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import SubscriptionChoices


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser, with additional fields for
    subscription management and UUID as primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    subscription = models.CharField(
        choices=SubscriptionChoices.choices(),
        max_length=8,
        editable=False
    )
