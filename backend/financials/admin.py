from django.contrib import admin

from .models import (
    ChannelPartner,
    APIKey
)


@admin.register(ChannelPartner)
class ChannelPartnerAdmin(
    admin.ModelAdmin
):

    list_display = (

        "company_name",

        "partner_id",

        "contact_email",

        "tier",

        "is_active"

    )


@admin.register(APIKey)
class APIKeyAdmin(
    admin.ModelAdmin
):

    list_display = (

        "key_id",

        "partner",

        "is_active",

        "created_at"

    )