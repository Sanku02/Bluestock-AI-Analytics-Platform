# backend/financials/models.py
from django.db import models

import uuid


class ChannelPartner(models.Model):

    TIER_CHOICES = [

        ("BASIC", "BASIC"),

        ("PRO", "PRO"),

        ("ENTERPRISE", "ENTERPRISE")

    ]   

    partner_id = models.UUIDField(

        default=uuid.uuid4,

        editable=False,

        unique=True

    )

    company_name = models.CharField(
        max_length=255
    )

    contact_email = models.EmailField(
        unique=True
    )

    tier = models.CharField(

        max_length=20,

        choices=TIER_CHOICES,

        default="BASIC"

    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def is_authenticated(self):
        return True

    def __str__(self):

        return self.company_name


class APIKey(models.Model):

    partner = models.ForeignKey(

        ChannelPartner,

        on_delete=models.CASCADE,

        related_name="api_keys"

    )

    key_id = models.UUIDField(

        default=uuid.uuid4,

        editable=False,

        unique=True

    )

    key_secret_hash = models.CharField(
        max_length=255
    )

    encrypted_secret = models.TextField(

        null=True,

        blank=True

    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    last_used_at = models.DateTimeField(

        null=True,

        blank=True

    )

    def __str__(self):

        return str(self.key_id)