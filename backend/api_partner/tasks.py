from celery import shared_task

from .models import APIUsageLog


@shared_task
def create_api_usage_log(

    partner_id,
    endpoint,
    method,
    status_code,
    response_time_ms,
    ip_address

):

    from financials.models import (
        ChannelPartner
    )

    partner = None

    if partner_id:

        try:

            partner = ChannelPartner.objects.get(
                id=partner_id
            )

        except ChannelPartner.DoesNotExist:

            partner = None

    APIUsageLog.objects.create(

        partner=partner,

        endpoint=endpoint,

        method=method,

        status_code=status_code,

        response_time_ms=response_time_ms,

        ip_address=ip_address

    )