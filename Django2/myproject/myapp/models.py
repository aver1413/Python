# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        verbose_name="Groups",
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_user_permissions",
        blank=True,
        verbose_name="User permissions",
        help_text="Specific permissions for this user.",
    )

