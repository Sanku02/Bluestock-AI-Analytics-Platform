from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.db.models import Q
from django.db import connection

from .models import (
    MLScoresLatest,
    MLScores,
    Company,
    Sector
)

from .serializers import (
    MLScoresLatestSerializer,
    MLScoresSerializer
)


# -----------------------------------
# ALL HEALTH SCORES
# -----------------------------------

@api_view(["GET"])
def health_scores(request):

    queryset = (
        MLScoresLatest.objects
        .all()
    )

    rating = request.GET.get(
        "rating"
    )

    if rating:

        queryset = queryset.filter(
            rating=rating.upper()
        )

    queryset = queryset.order_by(
        "-health_score"
    )

    serializer = (
        MLScoresLatestSerializer(
            queryset,
            many=True
        )
    )

    return Response(
        serializer.data
    )


# -----------------------------------
# TOP RATED COMPANIES
# -----------------------------------

@api_view(["GET"])
def top_rated(request):

    queryset = (

        MLScoresLatest.objects

        .filter(
            rating__in=[
                "EXCELLENT",
                "GOOD"
            ]
        )

        .order_by(
            "-health_score"
        )

    )

    serializer = (
        MLScoresLatestSerializer(
            queryset,
            many=True
        )
    )

    return Response(
        serializer.data
    )


# -----------------------------------
# WEAK COMPANIES
# -----------------------------------

@api_view(["GET"])
def weak_companies(request):

    queryset = (

        MLScoresLatest.objects

        .filter(
            rating__in=[
                "WEAK",
                "POOR"
            ]
        )

        .order_by(
            "health_score"
        )

    )

    serializer = (
        MLScoresLatestSerializer(
            queryset,
            many=True
        )
    )

    return Response(
        serializer.data
    )


# -----------------------------------
# COMPANY DETAIL API
# -----------------------------------

@api_view(["GET"])
def company_detail(
    request,
    symbol
):

    company = get_object_or_404(
        Company,
        symbol=symbol
    )

    latest_score = (

        MLScoresLatest.objects

        .filter(
            symbol=symbol
        )

        .first()

    )

    response = {

        "symbol":
            company.symbol,

        "company_name":
            company.company_name,

        "sector_id":
            company.sector_id,

        "roe_percentage":
            company.roe_percentage,

        "roce_percentage":
            company.roce_percentage,

        "health_score":
            (
                latest_score.health_score
                if latest_score
                else None
            ),

        "rating":
            (
                latest_score.rating
                if latest_score
                else None
            ),

        "computed_at":
            (
                latest_score.computed_at
                if latest_score
                else None
            )

    }

    return Response(response)


# -----------------------------------
# HISTORICAL SCORE TREND
# -----------------------------------

@api_view(["GET"])
def score_history(
    request,
    symbol
):

    queryset = (

        MLScores.objects

        .filter(
            symbol=symbol
        )

        .order_by(
            "computed_at"
        )

    )

    serializer = (
        MLScoresSerializer(
            queryset,
            many=True
        )
    )

    return Response(
        serializer.data
    )


# -----------------------------------
# SECTOR RANKINGS
# -----------------------------------

@api_view(["GET"])
def sector_rankings(request):

    results = []

    sectors = Sector.objects.all()

    for sector in sectors:

        companies = (

            Company.objects

            .filter(
                sector_id=sector.sector_id
            )

            .values_list(
                "symbol",
                flat=True
            )

        )

        scores = (

            MLScoresLatest.objects

            .filter(
                symbol__in=companies
            )

        )

        avg_score = (

            scores.aggregate(
                Avg("health_score")
            )["health_score__avg"]

        )

        results.append({

            "sector_name":
                sector.sector_name,

            "avg_health_score":
                round(avg_score, 2)
                if avg_score
                else None,

            "company_count":
                scores.count()

        })

    results = sorted(

        results,

        key=lambda x:
            x["avg_health_score"]
            or 0,

        reverse=True

    )

    return Response(results)


# -----------------------------------
# COMPANY SEARCH
# -----------------------------------

@api_view(["GET"])
def company_search(request):

    query = request.GET.get(
        "q",
        ""
    )

    companies = (

        Company.objects

        .filter(

            Q(symbol__icontains=query)

            |

            Q(company_name__icontains=query)

        )[:20]

    )

    results = [

        {

            "symbol":
                company.symbol,

            "company_name":
                company.company_name

        }

        for company in companies

    ]

    return Response(results)


# -----------------------------------
# TOP COMPANIES
# -----------------------------------

@api_view(["GET"])
def top_companies(request):

    queryset = (

        MLScoresLatest.objects

        .order_by(
            "-health_score"
        )[:10]

    )

    serializer = (

        MLScoresLatestSerializer(
            queryset,
            many=True
        )

    )

    return Response(
        serializer.data
    )


# -----------------------------------
# DASHBOARD SUMMARY
# -----------------------------------

@api_view(["GET"])
def dashboard_summary(request):

    queryset = (
        MLScoresLatest.objects
        .all()
    )

    total_companies = queryset.count()

    excellent_count = queryset.filter(
        rating="EXCELLENT"
    ).count()

    good_count = queryset.filter(
        rating="GOOD"
    ).count()

    average_count = queryset.filter(
        rating="AVERAGE"
    ).count()

    weak_count = queryset.filter(
        rating="WEAK"
    ).count()

    poor_count = queryset.filter(
        rating="POOR"
    ).count()

    top_company = queryset.order_by(
        "-health_score"
    ).first()

    cursor = connection.cursor()

    cursor.execute("""

    SELECT
        ds.sector_name,
        AVG(f.health_score) as avg_score

    FROM fact_ml_scores_latest f

    JOIN dim_company dc
        ON f.symbol = dc.symbol

    JOIN dim_sector ds
        ON dc.sector_id = ds.sector_id

    GROUP BY ds.sector_name
                   
    HAVING COUNT(f.symbol) >= 5              

    ORDER BY avg_score DESC

    LIMIT 1

""")

    sector_row = cursor.fetchone()

    top_sector = (
        sector_row[0]
        if sector_row
        else None
    )

    return Response({

        "total_companies":
            total_companies,

        "excellent_count":
            excellent_count,

        "good_count":
            good_count,

        "average_count":
            average_count,

        "weak_count":
            weak_count,

        "poor_count":
            poor_count,

        "top_company":
            (
                top_company.symbol
                if top_company
                else None
            ),

        "top_sector":
            top_sector

    })

@api_view(["GET"])
def sector_analysis(request):

    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            ds.sector_name,

            ROUND(
                AVG(f.health_score)::numeric,
                2
            ) as avg_score,

            COUNT(*) as company_count

        FROM fact_ml_scores_latest f

        JOIN dim_company dc
            ON f.symbol = dc.symbol

        JOIN dim_sector ds
            ON dc.sector_id = ds.sector_id

        GROUP BY ds.sector_name

        ORDER BY avg_score DESC

    """)

    rows = cursor.fetchall()

    results = []

    for row in rows:

        avg_score = float(row[1])

        if avg_score >= 85:
            rating = "EXCELLENT"

        elif avg_score >= 70:
            rating = "GOOD"

        elif avg_score >= 50:
            rating = "AVERAGE"

        elif avg_score >= 35:
            rating = "WEAK"

        else:
            rating = "POOR"

        results.append({

            "sector_name": row[0],

            "avg_score": avg_score,

            "company_count": row[2],

            "rating": rating

        })

    return Response(results)

@api_view(["GET"])
def ai_recommendations(request):

    strong_companies = (

        MLScoresLatest.objects

        .filter(
            rating__in=[
                "EXCELLENT",
                "GOOD"
            ]
        )

        .order_by(
            "-health_score"
        )[:5]

    )

    risky_companies = (

        MLScoresLatest.objects

        .filter(
            rating__in=[
                "WEAK",
                "POOR"
            ]
        )

        .order_by(
            "health_score"
        )[:5]

    )

    top_roe = (

        Company.objects

        .exclude(
            roe_percentage__isnull=True
        )

        .order_by(
            "-roe_percentage"
        )[:5]

    )

    top_picks_data = []

    for company in strong_companies:

        company_obj = Company.objects.filter(
            symbol=company.symbol
        ).first()

        top_picks_data.append({

            "symbol":
                company.symbol,

            "company_name":
                company_obj.company_name
                if company_obj
                else company.symbol,

            "health_score":
                company.health_score,

            "rating":
                company.rating

        })

    risky_data = []

    for company in risky_companies:

        company_obj = Company.objects.filter(
            symbol=company.symbol
        ).first()

        risky_data.append({

            "symbol":
                company.symbol,

            "company_name":
                company_obj.company_name
                if company_obj
                else company.symbol,

            "health_score":
                company.health_score,

            "rating":
                company.rating

        })

    high_roe_data = []

    for company in top_roe:

        high_roe_data.append({

            "symbol":
                company.symbol,

            "company_name":
                company.company_name,

            "roe":
                company.roe_percentage

        })

    return Response({

        "top_picks":
            top_picks_data,

        "risky_companies":
            risky_data,

        "high_roe":
            high_roe_data

    })