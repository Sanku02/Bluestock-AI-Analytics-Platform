# financials/authentication.py
import time

import hmac

import hashlib

import secrets

from cryptography.fernet import Fernet

from django.conf import settings

from rest_framework.authentication import (
    BaseAuthentication
)

from rest_framework.exceptions import (
    AuthenticationFailed
)

from .models import APIKey

from django.utils import timezone


class PartnerHMACAuthentication(
    BaseAuthentication
):

    def authenticate(
        self,
        request
    ):

        key_id = request.headers.get(
            "X-API-Key-ID"
        )

        timestamp = request.headers.get(
            "X-Timestamp"
        )

        signature = request.headers.get(
            "X-Signature"
        )

        nonce = request.headers.get(
            "X-Nonce"
        )

        if not all([

            key_id,
            timestamp,
            signature,
            nonce

        ]):

            raise AuthenticationFailed(
                "Missing authentication headers"
            )

        print("KEY_ID =", key_id)

        try:

            api_key = APIKey.objects.get(
                key_id=key_id,
                is_active=True
            )

            print("API KEY FOUND")

        except APIKey.DoesNotExist:

            print("API KEY NOT FOUND")

            raise AuthenticationFailed(
                "Invalid API Key"
            )

        current_time = int(
            time.time()
        )

        request_time = int(
            timestamp
        )

        if abs(
         current_time - request_time
        ) > 300:

            raise AuthenticationFailed(
                "Request expired"
            )

        cipher = Fernet(
            settings.FERNET_SECRET_KEY.encode()
        )

        secret_key = cipher.decrypt(
            api_key.encrypted_secret.encode()
        ).decode()

        body = request.body.decode()

        message = (

            request.method
            +
            request.path
            +
            timestamp
            +
            body

        )

        expected_signature = hmac.new(

            secret_key.encode(),

            message.encode(),

            hashlib.sha256

        ).hexdigest()

        print("RECEIVED =", signature)
        print("EXPECTED =", expected_signature)

        if not secrets.compare_digest(
            signature,
            expected_signature
        ):
            raise Exception(
                f"""
        RECEIVED: {signature}

        EXPECTED: {expected_signature}

        MESSAGE: {message}

        PATH: {request.path}
        """
            )

        api_key.last_used_at = timezone.now()

        api_key.save(update_fields=["last_used_at"])

        return (
            api_key.partner,
            None
        )