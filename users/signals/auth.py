from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from ..models import ApiUser


@receiver(post_save, sender=ApiUser)
def create_auth_token(sender: ApiUser, instance: ApiUser | None = None, created: bool = False, **kwargs: Any) -> None:
    """Create authentication token when a new user is created."""
    if created:
        Token.objects.create(user=instance)
