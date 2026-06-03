# backend/api_partner/urls.py
from django.urls import path

from .views import (
    partner_company_full,
    partner_company_health,
    partner_company_scores,
    partner_top_companies,
    partner_sector_rankings,
    partner_compare_companies,
    partner_top_movers,
    partner_sector_detail,
    partner_search_companies,
    partner_dashboard,
    partner_watchlist
)

urlpatterns = [

    path(
        "v1/companies/<str:symbol>/full/",
        partner_company_full,
        name="partner-company-full"
    ),

    path(
        "v1/companies/<str:symbol>/health/",
        partner_company_health,
        name="partner-company-health"
    ),

    path(
        "v1/companies/<str:symbol>/scores/",
        partner_company_scores,
        name="partner-company-scores"
    ),

    path(
        "v1/top-companies/",
        partner_top_companies,
        name="partner-top-companies"
    ),

    path(
        "v1/sector-rankings/",
        partner_sector_rankings,
        name="partner-sector-rankings"
    ),

    path(
        "v1/compare/",
        partner_compare_companies,
        name="partner-compare-companies"
    ),

    path(
        "v1/top-movers/",
        partner_top_movers,
        name="partner-top-movers"
    ),

    path(
        "v1/sector/<str:sector_name>/",
        partner_sector_detail,
        name="partner-sector-detail"
    ),

    path(
        "v1/search/",
        partner_search_companies,
        name="partner-search"
    ),

    path(
        "v1/dashboard/",
        partner_dashboard,
        name="partner-dashboard"
    ),

    path(
        "v1/watchlist/",
        partner_watchlist,
        name="partner-watchlist"
    ),

]