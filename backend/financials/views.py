#backend/financials/views.py
from rest_framework.decorators import (
    api_view,
    authentication_classes
)

from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django.conf import settings

from cryptography.fernet import Fernet

from .models import (
    ChannelPartner,
    APIKey
)

from .authentication import (
    PartnerHMACAuthentication
)

import bcrypt

import secrets

import uuid


@api_view(["POST"])
def generate_partner_api_key(
    request,
    partner_id
):

    partner = get_object_or_404(
    ChannelPartner,
    partner_id=partner_id
    )

    key_id = str(
        uuid.uuid4()
    )

    raw_secret = secrets.token_hex(32)

    hashed_secret = bcrypt.hashpw(
        raw_secret.encode(),
        bcrypt.gensalt()
    ).decode()

    cipher = Fernet(
        settings.FERNET_SECRET_KEY.encode()
    )

    encrypted_secret = cipher.encrypt(
        raw_secret.encode()
    ).decode()

    api_key = APIKey.objects.create(

        partner=partner,

        key_id=key_id,

        key_secret_hash=hashed_secret,

        encrypted_secret=encrypted_secret

    )

    return Response({

        "key_id":
            key_id,

        "key_secret":
            raw_secret,

       "message":
         "Save this API secret securely. "
         "It cannot be recovered later."

    })


@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
def secure_test(
    request
):

    return Response({

        "message":
            "Authenticated successfully",

        "partner":
            request.user.company_name

    })