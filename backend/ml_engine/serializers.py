from rest_framework import serializers

from .models import MLScoresLatest


from .models import Company

from .models import MLScores


class MLScoresLatestSerializer(
    serializers.ModelSerializer
):

    company_name = serializers.SerializerMethodField()

    class Meta:

        model = MLScoresLatest

        fields = [

            "symbol",

            "company_name",

            "health_score",

            "rating",

            "computed_at"

        ]

    def get_company_name(
        self,
        obj
    ):

        company = Company.objects.filter(
            symbol=obj.symbol
        ).first()

        if company:

            return company.company_name

        return obj.symbol




class CompanySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Company

        fields = "__all__"




class MLScoresSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = MLScores

        fields = "__all__"