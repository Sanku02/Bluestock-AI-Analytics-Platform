import json

import hmac

import hashlib

import requests

from django.utils import timezone

from api_partner.models import (

    WebhookEndpoint,
    WebhookDeliveryLog

)


def generate_signature(

    secret,
    payload

):

    return hmac.new(

        secret.encode(),

        json.dumps(payload).encode(),

        hashlib.sha256

    ).hexdigest()


def dispatch_webhook(

    event_type,
    payload

):

    webhooks = WebhookEndpoint.objects.filter(

        subscribed_event=event_type,

        is_active=True

    )

    for webhook in webhooks:

        signature = generate_signature(

            webhook.secret_key,

            payload

        )

        try:

            response = requests.post(

                webhook.target_url,

                json=payload,

                headers={

                    "X-Bluestock-Signature":
                        signature,

                    "Content-Type":
                        "application/json"

                },

                timeout=10

            )

            WebhookDeliveryLog.objects.create(

                webhook=webhook,

                event_type=event_type,

                payload=payload,

                response_status=response.status_code,

                response_body=response.text,

                delivered=(
                    200 <= response.status_code < 300
                ),

                delivered_at=timezone.now()

            )

        except Exception as e:

            WebhookDeliveryLog.objects.create(

                webhook=webhook,

                event_type=event_type,

                payload=payload,

                response_body=str(e),

                delivered=False

            )