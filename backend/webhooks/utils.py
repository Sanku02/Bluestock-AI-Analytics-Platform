from .tasks import (
    send_webhook_event
)


def trigger_health_update_webhook(

    company

):

    payload = {

        "symbol":
            company.symbol,

        "company_name":
            company.company_name,

        "health_score":
            company.health_score,

        "rating":
            company.rating

    }

    send_webhook_event.delay(

        "health.updated",
        payload
    )