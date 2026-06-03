from django.contrib import admin

from django.urls import (
    path,
    include
)

from drf_spectacular.views import (

    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView

)

urlpatterns = [

    # ADMIN

    path(
        "admin/",
        admin.site.urls
    ),

    # CORE INTERNAL APIs

    path(
        "api/",
        include("ml_engine.urls")
    ),

    path(
        "api/",
        include("financials.urls")
    ),

    # PARTNER APIs

    path(
        "api/partner/",
        include("api_partner.urls")
    ),

    # API DOCUMENTATION

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc"
    ),

    path(
    "api/webhooks/",
    include("webhooks.urls")
    ),

    path(
    "api/admin-insights/",
    include("admin_insights.urls")
    ),

]