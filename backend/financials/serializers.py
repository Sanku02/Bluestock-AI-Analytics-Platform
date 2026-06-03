#backend/financials/serializers.py
from rest_framework import serializers

from .models import (
    ChannelPartner,
    APIKey
)


class ChannelPartnerSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ChannelPartner

        fields = "__all__"


class APIKeySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = APIKey

        fields = "__all__"