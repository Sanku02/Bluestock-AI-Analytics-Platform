from django.urls import path

from .views import (
    company_detail,
    health_scores,
    top_rated,
    weak_companies, 
    score_history,
    sector_rankings,
    company_search,
    top_companies,
    dashboard_summary,
    sector_analysis,
    ai_recommendations,
)

urlpatterns = [

    path(
        "health-scores/",
        health_scores
    ),

    path(
        "top-rated/",
        top_rated
    ),

    path(
        "weak-companies/",
        weak_companies
    ),

    path(
    "company/<str:symbol>/",
    company_detail
    ),

    path(
    "score-history/<str:symbol>/",
    score_history
    ),
    
    path(
    "sector-rankings/",
    sector_rankings
    ),

    path(
    "search/",
    company_search
    ),

    path(
    "top-companies/",
    top_companies
    ),

    path(
    "dashboard-summary/",
    dashboard_summary
    ),

    path(
    "sector-analysis/",
    sector_analysis
 ),

path(
    "ai-recommendations/",
    ai_recommendations
),
    
]