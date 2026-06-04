import time

from .tasks import (
    create_api_usage_log
)


class PartnerAPILoggingMiddleware:

    def __init__(
        self,
        get_response
    ):
        self.get_response = get_response

    def __call__(
        self,
        request
    ):

        start_time = time.time()

        response = self.get_response(
            request
        )

        # Log every API request

        if request.path.startswith("/api/"):

            response_time = (
                time.time() - start_time
            ) * 1000

            partner_id = None

            if (
                hasattr(request, "user")
                and getattr(request.user, "is_authenticated", False)
            ):

                partner_id = request.user.id

            try:

                create_api_usage_log.delay(

                    partner_id=partner_id,

                    endpoint=request.path,

                    method=request.method,

                    status_code=response.status_code,

                    response_time_ms=round(
                        response_time,
                        2
                    ),

                    ip_address=request.META.get(
                        "REMOTE_ADDR"
                    )

                )

            except Exception as e:

                print(
                    f"API logging failed: {e}"
                )

        return response