from django.db import models

from financials.models import (
    ChannelPartner
)


class APIUsageLog(models.Model):

    partner = models.ForeignKey(

        ChannelPartner,

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    endpoint = models.CharField(
        max_length=255
    )

    method = models.CharField(
        max_length=20
    )

    status_code = models.IntegerField()

    response_time_ms = models.FloatField()

    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True

    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return (

            f"{self.endpoint} "
            f"{self.status_code}"
        )


class WebhookEndpoint(models.Model):

    EVENT_CHOICES = [

        ("health.updated", "health.updated"),

        ("company.updated", "company.updated"),

        ("sector.updated", "sector.updated")

    ]

    partner = models.ForeignKey(

        ChannelPartner,

        on_delete=models.CASCADE,

        related_name="webhooks"

    )

    target_url = models.URLField()

    secret_key = models.CharField(
        max_length=255
    )

    subscribed_event = models.CharField(

        max_length=100,

        choices=EVENT_CHOICES

    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (

            f"{self.partner.company_name} "
            f"- {self.subscribed_event}"
        )


class WebhookDeliveryLog(models.Model):

    webhook = models.ForeignKey(

        WebhookEndpoint,

        on_delete=models.CASCADE,

        related_name="deliveries"

    )

    event_type = models.CharField(
        max_length=100
    )

    payload = models.JSONField()

    response_status = models.IntegerField(

        null=True,

        blank=True

    )

    response_body = models.TextField(

        null=True,

        blank=True

    )

    retry_count = models.IntegerField(
        default=0
    )

    delivered = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    delivered_at = models.DateTimeField(

        null=True,

        blank=True

    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return (

            f"{self.event_type} "
            f"- {self.delivered}"
        )