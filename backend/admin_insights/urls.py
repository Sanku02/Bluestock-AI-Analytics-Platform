from django.urls import path

from .views import (

    api_usage_overview,
    top_api_endpoints,
    webhook_delivery_overview,
    failed_webhooks,

    dashboard,
    health_monitor,
    api_analytics,
    webhooks_dashboard,
    celery_monitor,
    data_quality_view,
    api_management,
    anomalies_view,
    bulk_import_view,
    company_detail

)

urlpatterns = [

    path(
        "",
        dashboard,
        name="admin-dashboard"
    ),

    path(
        "health-monitor/",
        health_monitor,
        name="health-monitor"
    ),

    path(
        "api-analytics/",
        api_analytics,
        name="api-analytics"
    ),

    path(
        "webhooks/",
        webhooks_dashboard,
        name="webhooks-dashboard"
    ),

    path(
        "celery-monitor/",
        celery_monitor,
        name="celery-monitor"
    ),

    path(
        "usage-overview/",
        api_usage_overview
    ),

    path(
        "top-endpoints/",
        top_api_endpoints
    ),

    path(
        "webhook-overview/",
        webhook_delivery_overview
    ),

    path(
        "failed-webhooks/",
        failed_webhooks
    ),

    path(
    "data-quality/",
    data_quality_view
    ),

    path(
    "api-management/",
    api_management
    ),

    path(
    "anomalies/",
    anomalies_view
    ),

    path(
    "bulk-import/",
    bulk_import_view,
    name="bulk-import"
    ),

    path(
    "company/<str:symbol>/",
    company_detail,
    name="company-detail"
),

]