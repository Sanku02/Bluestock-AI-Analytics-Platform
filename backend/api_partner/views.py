#backend/api_partner/views.py
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    throttle_classes
)

from rest_framework.response import Response

from rest_framework.exceptions import NotFound

from financials.authentication import (
    PartnerHMACAuthentication
)

from financials.throttles import (
    PartnerRateThrottle
)

from django.db.models import Q

from .serializers import (
    PartnerCompanySerializer,
    PartnerHealthSerializer,
    PartnerScoreHistorySerializer,
    TopCompanySerializer,
    SectorRankingSerializer,
    CompanyComparisonSerializer,
    TopMoverSerializer,
    SectorCompanySerializer,
    CompanySearchSerializer,
    DashboardSerializer,
    WatchlistSerializer
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter
)

from ml_engine.models import (
    MLScoresLatest,
    MLScores,
    Company,
    Sector
)

# ---------------------------------------------------
# COMPANY FULL DETAILS
# ---------------------------------------------------

@extend_schema(

    summary="Company Full Details",

    description="Returns complete company profile details",

    responses={
        200: PartnerCompanySerializer
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_company_full(
    request,
    symbol
):

    company = Company.objects.filter(
        symbol__iexact=symbol
    ).first()

    if not company:

        raise NotFound(
            "Company not found"
        )

    serializer = PartnerCompanySerializer(
        company
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# COMPANY HEALTH
# ---------------------------------------------------

@extend_schema(

    summary="Company Health Score",

    description="Returns latest ML health score for a company",

    responses={
        200: PartnerHealthSerializer
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_company_health(
    request,
    symbol
):

    company = Company.objects.filter(
        symbol__iexact=symbol
    ).first()

    if not company:

        raise NotFound(
            "Company not found"
        )

    latest_score = MLScoresLatest.objects.filter(
        symbol__iexact=symbol
    ).first()

    if not latest_score:

        raise NotFound(
            "Health score not found"
        )

    data = {

        "symbol": company.symbol,

        "company_name": company.company_name,

        "health_score": latest_score.health_score,

        "rating": latest_score.rating,

        "computed_at": latest_score.computed_at
    }

    serializer = PartnerHealthSerializer(
        data
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# HISTORICAL SCORES
# ---------------------------------------------------

@extend_schema(

    summary="Historical ML Scores",

    description="Returns historical ML scores for a company",

    responses={
        200: PartnerScoreHistorySerializer(
            many=True
        )
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_company_scores(
    request,
    symbol
):

    scores = MLScores.objects.filter(
        symbol__iexact=symbol
    ).order_by(
        "-computed_at"
    )[:50]

    serializer = PartnerScoreHistorySerializer(
        scores,
        many=True
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# TOP COMPANIES
# ---------------------------------------------------

@extend_schema(

    summary="Top Companies",

    description="Returns highest ranked companies",

    responses={
        200: TopCompanySerializer(
            many=True
        )
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_top_companies(
    request
):

    scores = MLScoresLatest.objects.order_by(
        "-health_score"
    )[:20]

    results = []

    for score in scores:

        company = Company.objects.filter(
            symbol=score.symbol
        ).first()

        if company:

            results.append({

                "symbol":
                    score.symbol,

                "company_name":
                    company.company_name,

                "health_score":
                    score.health_score,

                "rating":
                    score.rating
            })

    serializer = TopCompanySerializer(
        results,
        many=True
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# SECTOR RANKINGS
# ---------------------------------------------------

@extend_schema(

    summary="Sector Rankings",

    description="Returns sectors ranked by average health score",

    responses={
        200: SectorRankingSerializer(
            many=True
        )
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_sector_rankings(
    request
):

    companies = Company.objects.all()

    sector_scores = {}

    for company in companies:

        latest_score = MLScoresLatest.objects.filter(
            symbol=company.symbol
        ).first()

        if latest_score:

            sector = Sector.objects.filter(
                sector_id=company.sector_id
            ).first()

            if sector:

                if sector.sector_name not in sector_scores:

                    sector_scores[
                        sector.sector_name
                    ] = []

                sector_scores[
                    sector.sector_name
                ].append(
                    latest_score.health_score
                )

    results = []

    for sector_name, scores in sector_scores.items():

        average_score = sum(scores) / len(scores)

        results.append({

            "sector_name":
                sector_name,

            "average_health_score":
                round(average_score, 2)
        })

    results = sorted(

        results,

        key=lambda x:
            x["average_health_score"],

        reverse=True
    )

    serializer = SectorRankingSerializer(
        results,
        many=True
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# COMPARE COMPANIES
# ---------------------------------------------------

@extend_schema(

    summary="Compare Companies",

    description="Compare multiple companies",

    parameters=[

        OpenApiParameter(

            name="symbols",

            type=str,

            location=OpenApiParameter.QUERY,

            description="Comma separated symbols"
        )
    ],

    responses={
        200: CompanyComparisonSerializer(
            many=True
        )
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_compare_companies(
    request
):

    symbols = request.GET.get(
        "symbols",
        ""
    )

    symbols_list = [

        s.strip().upper()

        for s in symbols.split(",")

        if s.strip()
    ]

    results = []

    for symbol in symbols_list:

        company = Company.objects.filter(
            symbol__iexact=symbol
        ).first()

        latest_score = MLScoresLatest.objects.filter(
            symbol__iexact=symbol
        ).first()

        if company and latest_score:

            results.append({

                "symbol":
                    company.symbol,

                "company_name":
                    company.company_name,

                "health_score":
                    latest_score.health_score,

                "rating":
                    latest_score.rating,

                "roe_percentage":
                    company.roe_percentage,

                "roce_percentage":
                    company.roce_percentage
            })

    serializer = CompanyComparisonSerializer(
        results,
        many=True
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# TOP MOVERS
# ---------------------------------------------------

@extend_schema(

    summary="Top Movers",

    description="Returns top gainers and decliners"
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_top_movers(
    request
):

    top_companies = MLScoresLatest.objects.order_by(
        "-health_score"
    )[:5]

    low_companies = MLScoresLatest.objects.order_by(
        "health_score"
    )[:5]

    gainers = []

    decliners = []

    for item in top_companies:

        company = Company.objects.filter(
            symbol__iexact=item.symbol
        ).first()

        gainers.append({

            "symbol":
                item.symbol,

            "company_name":
                company.company_name if company else None,

            "health_score":
                item.health_score,

            "rating":
                item.rating
        })

    for item in low_companies:

        company = Company.objects.filter(
            symbol__iexact=item.symbol
        ).first()

        decliners.append({

            "symbol":
                item.symbol,

            "company_name":
                company.company_name if company else None,

            "health_score":
                item.health_score,

            "rating":
                item.rating
        })

    return Response({

        "top_gainers":
            TopMoverSerializer(
                gainers,
                many=True
            ).data,

        "top_decliners":
            TopMoverSerializer(
                decliners,
                many=True
            ).data
    })


# ---------------------------------------------------
# SECTOR DETAILS
# ---------------------------------------------------

@extend_schema(

    summary="Sector Details",

    description="Returns companies inside a sector"
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_sector_detail(
    request,
    sector_name
):

    sector = Sector.objects.filter(
        sector_name__iexact=sector_name
    ).first()

    if not sector:

        return Response({
            "detail": "Sector not found"
        }, status=404)

    companies = Company.objects.filter(
        sector_id=sector.sector_id
    )

    results = []

    scores = []

    for company in companies:

        latest_score = MLScoresLatest.objects.filter(
            symbol__iexact=company.symbol
        ).first()

        if latest_score:

            scores.append(
                latest_score.health_score
            )

            results.append({

                "symbol":
                    company.symbol,

                "company_name":
                    company.company_name,

                "health_score":
                    latest_score.health_score,

                "rating":
                    latest_score.rating
            })

    avg_score = (

        sum(scores) / len(scores)

        if scores else 0
    )

    serializer = SectorCompanySerializer(
        results,
        many=True
    )

    return Response({

        "sector_name":
            sector.sector_name,

        "average_health_score":
            round(avg_score, 2),

        "companies":
            serializer.data
    })


# ---------------------------------------------------
# SEARCH COMPANIES
# ---------------------------------------------------

@extend_schema(

    summary="Search Companies",

    description="Search companies by symbol or company name",

    parameters=[

        OpenApiParameter(

            name="query",

            type=str,

            location=OpenApiParameter.QUERY,

            description="Search keyword"
        )
    ],

    responses={
        200: CompanySearchSerializer(
            many=True
        )
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_search_companies(
    request
):

    query = request.GET.get(
        "query",
        ""
    )

    companies = Company.objects.filter(

        Q(symbol__icontains=query)

        |

        Q(company_name__icontains=query)

    )[:10]

    results = []

    for company in companies:

        results.append({

            "symbol":
                company.symbol,

            "company_name":
                company.company_name
        })

    serializer = CompanySearchSerializer(
        results,
        many=True
    )

    return Response(
        serializer.data
    )


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

@extend_schema(

    summary="Partner Dashboard",

    description="Returns platform analytics summary",

    responses={
        200: DashboardSerializer
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_dashboard(request):

    latest_scores = (
        MLScoresLatest.objects.all()
    )

    total_companies = (
        latest_scores.count()
    )

    excellent_count = (
        latest_scores.filter(
            rating="EXCELLENT"
        ).count()
    )

    good_count = (
        latest_scores.filter(
            rating="GOOD"
        ).count()
    )

    average_count = (
        latest_scores.filter(
            rating="AVERAGE"
        ).count()
    )

    weak_count = (
        latest_scores.filter(
            rating="WEAK"
        ).count()
    )

    poor_count = (
        latest_scores.filter(
            rating="POOR"
        ).count()
    )

    top_company_obj = (
        latest_scores
        .order_by("-health_score")
        .first()
    )

    top_company = (
        top_company_obj.symbol
        if top_company_obj
        else "N/A"
    )

    sector_scores = {}

    companies = Company.objects.all()

    for company in companies:

        latest_score = (
            MLScoresLatest.objects.filter(
                symbol=company.symbol
            ).first()
        )

        if not latest_score:

            continue

        sector = Sector.objects.filter(
            sector_id=company.sector_id
        ).first()

        if not sector:

            continue

        sector_name = sector.sector_name

        if sector_name not in sector_scores:

            sector_scores[sector_name] = []

        sector_scores[sector_name].append(
            latest_score.health_score
        )

    top_sector = "N/A"

    best_avg_score = 0

    all_scores = []

    for sector_name, scores in sector_scores.items():

        avg_score = (
            sum(scores) / len(scores)
        )

        all_scores.extend(scores)

        if avg_score > best_avg_score:

            best_avg_score = avg_score

            top_sector = sector_name

    overall_average = (

        sum(all_scores) / len(all_scores)

        if all_scores else 0

    )

    data = {

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
            top_company,

        "top_sector":
            top_sector,

        "average_health_score":
            round(overall_average, 2)

    }

    return Response(data)

# ---------------------------------------------------
# WATCHLIST
# ---------------------------------------------------

@extend_schema(

    summary="Watchlist API",

    description="Returns analytics for watchlist companies",

    parameters=[

        OpenApiParameter(

            name="symbols",

            type=str,

            location=OpenApiParameter.QUERY,

            description="Comma separated symbols"
        )
    ],

    responses={
        200: WatchlistSerializer(
            many=True
        )
    }
)

@api_view(["GET"])
@authentication_classes([
    PartnerHMACAuthentication
])
@throttle_classes([
    PartnerRateThrottle
])

def partner_watchlist(
    request
):

    symbols = request.GET.get(
        "symbols",
        ""
    )

    symbol_list = [

        s.strip().upper()

        for s in symbols.split(",")

        if s.strip()
    ]

    results = []

    for symbol in symbol_list:

        company = Company.objects.filter(
            symbol__iexact=symbol
        ).first()

        latest_score = MLScoresLatest.objects.filter(
            symbol__iexact=symbol
        ).first()

        if company and latest_score:

            results.append({

                "symbol":
                    symbol,

                "company_name":
                    company.company_name,

                "health_score":
                    latest_score.health_score,

                "rating":
                    latest_score.rating
            })

    serializer = WatchlistSerializer(
        results,
        many=True
    )

    return Response(
        serializer.data
    )