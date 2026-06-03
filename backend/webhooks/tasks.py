from celery import shared_task

from api_partner.models import (
    WebhookDeliveryLog
)

from .services import (
    dispatch_webhook
)


@shared_task
def send_webhook_event(

    event_type,
    payload

):

    dispatch_webhook(

        event_type,
        payload
    )


@shared_task(
    bind=True,
    max_retries=3
)
def retry_failed_webhook(

    self,
    delivery_log_id

):

    try:

        log = WebhookDeliveryLog.objects.get(
            id=delivery_log_id
        )

        webhook = log.webhook

        dispatch_webhook(

            log.event_type,
            log.payload
        )

        log.retry_count += 1

        log.save()

    except Exception as exc:

        raise self.retry(

            exc=exc,

            countdown=60
        )