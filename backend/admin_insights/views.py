import json

from django.db.models import (
    Count,
    Avg
)
from companies.models import (BalanceSheet, ProfitLoss)

from services.postgres_service import (
    write_dataframe
)

from django.db import connection

from django.shortcuts import render

from django.contrib.admin.views.decorators import (
    staff_member_required
)

import pandas as pd

from .forms import BulkImportForm

from ml_engine.models import (
    MLScoresLatest,
    MLScores,
    Company,
    Sector, 
    Anomaly
)

from financials.models import (
    ChannelPartner,
    APIKey
)

from django_celery_beat.models import (
    PeriodicTask
)

from rest_framework.decorators import (
    api_view
)

from rest_framework.response import (
    Response
)

from api_partner.models import (
    APIUsageLog,
    WebhookDeliveryLog
)


# --------------------------------------------------
# API INSIGHT ENDPOINTS
# --------------------------------------------------

@api_view(["GET"])
def api_usage_overview(request):

    total_requests = APIUsageLog.objects.count()

    successful_requests = (
        APIUsageLog.objects.filter(
            status_code__lt=400
        ).count()
    )

    failed_requests = (
        APIUsageLog.objects.filter(
            status_code__gte=400
        ).count()
    )

    avg_response_time = (
        APIUsageLog.objects.aggregate(
            avg=Avg("response_time_ms")
        )["avg"]
    )

    return Response({

        "total_requests":
            total_requests,

        "successful_requests":
            successful_requests,

        "failed_requests":
            failed_requests,

        "average_response_time_ms":
            round(
                avg_response_time or 0,
                2
            )

    })


@api_view(["GET"])
def top_api_endpoints(request):

    endpoints = (

        APIUsageLog.objects.values(
            "endpoint"
        )

        .annotate(
            total_hits=Count("id")
        )

        .order_by("-total_hits")[:10]
    )

    return Response(endpoints)


@api_view(["GET"])
def webhook_delivery_overview(request):

    total_webhooks = (
        WebhookDeliveryLog.objects.count()
    )

    successful_deliveries = (
        WebhookDeliveryLog.objects.filter(
            delivered=True
        ).count()
    )

    failed_deliveries = (
        WebhookDeliveryLog.objects.filter(
            delivered=False
        ).count()
    )

    return Response({

        "total_webhooks":
            total_webhooks,

        "successful_deliveries":
            successful_deliveries,

        "failed_deliveries":
            failed_deliveries

    })


@api_view(["GET"])
def failed_webhooks(request):

    failures = (

        WebhookDeliveryLog.objects.filter(
            delivered=False
        )

        .values(

            "event_type",
            "response_body",
            "created_at"

        )[:20]
    )

    return Response(failures)


# --------------------------------------------------
# EXECUTIVE DASHBOARD
# --------------------------------------------------

@staff_member_required
def dashboard(request):

    avg_score = (
        MLScoresLatest.objects.aggregate(
            avg=Avg("health_score")
        )["avg"]
    )

    anomalies = Anomaly.objects.filter(
        final_anomaly=True
    ).count()

    context = {

        "total_companies":
            Company.objects.count(),

        "avg_score":
            round(
                avg_score or 0,
                2
            ),

        "excellent":
            MLScoresLatest.objects.filter(
                rating="EXCELLENT"
            ).count(),

        "good":
            MLScoresLatest.objects.filter(
                rating="GOOD"
            ).count(),

        "average":
            MLScoresLatest.objects.filter(
                rating="AVERAGE"
            ).count(),

        "weak":
            MLScoresLatest.objects.filter(
                rating="WEAK"
            ).count(),

        "poor":
            MLScoresLatest.objects.filter(
                rating="POOR"
            ).count(),

        "sector_count":
            Sector.objects.count(),

        "anomalies":
            anomalies

    }

    return render(
        request,
        "admin_insights/dashboard.html",
        context
    )


# --------------------------------------------------
# HEALTH MONITOR
# --------------------------------------------------

@staff_member_required
def health_monitor(request):

    companies = (

        MLScoresLatest.objects
        .all()
        .order_by("-health_score")

    )

    return render(

        request,

        "admin_insights/health_monitor.html",

        {
            "companies": companies
        }
    )


# --------------------------------------------------
# API ANALYTICS
# --------------------------------------------------

@staff_member_required
def api_analytics(request):

    endpoints = (

        APIUsageLog.objects.values(
            "endpoint"
        )

        .annotate(
            total=Count("id")
        )

        .order_by("-total")
    )

    return render(

        request,

        "admin_insights/api_analytics.html",

        {

            "total_calls":
                APIUsageLog.objects.count(),

            "success":
                APIUsageLog.objects.filter(
                    status_code__lt=400
                ).count(),

            "failed":
                APIUsageLog.objects.filter(
                    status_code__gte=400
                ).count(),

            "endpoints":
                endpoints
        }
    )


# --------------------------------------------------
# WEBHOOKS
# --------------------------------------------------

@staff_member_required
def webhooks_dashboard(request):

    return render(

        request,

        "admin_insights/webhooks.html",

        {

            "deliveries":

                WebhookDeliveryLog.objects.all()[:50]

        }
    )


# --------------------------------------------------
# CELERY MONITOR
# --------------------------------------------------

@staff_member_required
def celery_monitor(request):

    return render(

        request,

        "admin_insights/celery_monitor.html",

        {

            "tasks":

                PeriodicTask.objects.all()

        }
    )


# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

@staff_member_required
def data_quality_view(request):

    with connection.cursor() as cursor:

        cursor.execute("""

            SELECT

                c.company_name,
                y.year,

                CASE

                    WHEN bs.symbol IS NOT NULL
                    THEN 1

                    ELSE 0

                END

            FROM dim_company c

            CROSS JOIN dim_year y

            LEFT JOIN fact_balance_sheet bs

                ON bs.symbol = c.symbol

                AND bs.year_id = y.year_id

            ORDER BY c.company_name, y.year

        """)

        rows = cursor.fetchall()

    return render(

        request,

        "admin_insights/data_quality.html",

        {
            "rows": rows
        }
    )


# --------------------------------------------------
# API MANAGEMENT
# --------------------------------------------------

@staff_member_required
def api_management(request):

    partners = ChannelPartner.objects.all()

    partner_data = []

    for partner in partners:

        api_keys = APIKey.objects.filter(
            partner=partner
        )

        active_keys = api_keys.filter(
            is_active=True
        ).count()

        partner_data.append({

            "company_name":
                partner.company_name,

            "tier":
                partner.tier,

            "is_active":
                partner.is_active,

            "active_keys":
                active_keys,

            "created_at":
                partner.created_at

        })

    return render(

        request,

        "admin_insights/api_management.html",

        {
            "partners": partner_data
        }

    )


def anomalies_view(request):

    with connection.cursor() as cursor:

        cursor.execute("""

            SELECT

                symbol,
                year_id,
                anomaly_z_any,
                anomaly_iso,
                final_anomaly

            FROM fact_anomalies

            WHERE final_anomaly = TRUE

            ORDER BY anomaly_iso DESC

            LIMIT 200

        """)

        columns = [

            col[0]
            for col in cursor.description

        ]

        anomalies = [

            dict(zip(columns, row))
            for row in cursor.fetchall()

        ]

    return render(

        request,

        "admin_insights/anomalies.html",

        {
            "anomalies": anomalies
        }

    )

@staff_member_required
def bulk_import_view(request):

    preview = None
    success = None
    error = None

    if request.method == "POST":

        form = BulkImportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            csv_file = request.FILES["csv_file"]

            df = pd.read_csv(csv_file)

            selected_table = form.cleaned_data[
                "table_name"
            ]

            required_columns = {

                "fact_balance_sheet": [
                    "symbol",
                    "year_id"
                ],

                "fact_profit_loss": [
                    "symbol",
                    "year_id"
                ],

                "fact_cash_flow": [
                    "symbol",
                    "year_id"
                ]

            }

            expected = required_columns[
                selected_table
            ]

            missing = [

                col

                for col in expected

                if col not in df.columns

            ]

            if missing:

                error = (
                    f"Missing columns: {missing}"
                )

            else:

                if "import" in request.POST:

                    write_dataframe(
                        df,
                        selected_table,
                        if_exists="replace"
                    )

                    success = (
                        f"{len(df)} rows imported successfully into "
                        f"{selected_table}"
                    )

                preview = df.head(20).to_html(
                    classes="table",
                    index=False
                )

    else:

        form = BulkImportForm()

    return render(

        request,

        "admin_insights/bulk_import.html",

        {

            "form": form,

            "preview": preview,

            "success": success,

            "error": error

        }

    )

@staff_member_required
def company_detail(request, symbol):

    company = Company.objects.get(
        symbol=symbol
    )

    sector = Sector.objects.filter(
        sector_id=company.sector_id
    ).first()

    latest_score = MLScoresLatest.objects.filter(
        symbol=symbol
    ).first()

    latest_balance = BalanceSheet.objects.filter(
    symbol=symbol
    ).order_by("-year_id").first()

    latest_pl = ProfitLoss.objects.filter(
    symbol=symbol
    ).order_by("-year_id").first()

    anomaly_records = Anomaly.objects.filter(
        symbol=symbol,
        final_anomaly=True
    )

    history = MLScores.objects.filter(
        symbol=symbol
    ).order_by("-computed_at")

    score_dates = json.dumps([
    row.computed_at.strftime("%d-%b")
    for row in history
    ])

    score_values = json.dumps([
    float(row.health_score)
    for row in history
    ])

    anomalies = anomaly_records.count()

    return render(

        request,

        "admin_insights/company_detail.html",

        {

            "company": company,
            "sector": sector,
            "latest_score": latest_score,
            "anomalies": anomalies,
            "anomaly_records": anomaly_records,
            "history": history,
            "score_dates": score_dates,
            "score_values": score_values,
            "latest_balance": latest_balance,
            "latest_pl": latest_pl,

        }

    )
