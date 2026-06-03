from rest_framework.throttling import SimpleRateThrottle


class PartnerRateThrottle(
    SimpleRateThrottle
):

    scope = "partner"

    def get_cache_key(
        self,
        request,
        view
    ):

        api_key = request.headers.get(
            "X-API-Key-ID"
        )

        if not api_key:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": api_key
        }