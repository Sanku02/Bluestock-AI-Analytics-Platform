# backend/api_partner/serializers.py
from rest_framework import serializers

from companies.models import Company


class PartnerCompanySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Company

        fields = "__all__"


class PartnerHealthSerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()

    computed_at = serializers.DateTimeField()

class PartnerScoreHistorySerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()

    computed_at = serializers.DateTimeField()

class TopCompanySerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()

class SectorRankingSerializer(
    serializers.Serializer
):

    sector_name = serializers.CharField()

    average_health_score = serializers.FloatField()

class CompanyComparisonSerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()

    roe_percentage = serializers.FloatField()

    roce_percentage = serializers.FloatField()


class TopMoverSerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()

class SectorCompanySerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()

class CompanySearchSerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

class DashboardSerializer(
    serializers.Serializer
):

    total_companies = serializers.IntegerField()

    average_health_score = serializers.FloatField()

    top_sector = serializers.CharField()

    top_company = serializers.CharField()

class WatchlistSerializer(
    serializers.Serializer
):

    symbol = serializers.CharField()

    company_name = serializers.CharField()

    health_score = serializers.FloatField()

    rating = serializers.CharField()