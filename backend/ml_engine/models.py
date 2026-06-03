from django.db import models


# -----------------------------------
# LATEST SCORES TABLE
# -----------------------------------

class MLScoresLatest(models.Model):

    symbol = models.CharField(
        max_length=20,
        primary_key=True
    )

    health_score = models.FloatField()

    rating = models.CharField(
        max_length=20
    )

    computed_at = models.DateTimeField()

    class Meta:

        managed = False

        db_table = "fact_ml_scores_latest"


# -----------------------------------
# HISTORICAL SCORES TABLE
# -----------------------------------

class MLScores(models.Model):

    symbol = models.CharField(
        max_length=20
    )

    health_score = models.FloatField()

    rating = models.CharField(
        max_length=20
    )

    computed_at = models.DateTimeField(
        primary_key=True
    )

    class Meta:

        managed = False

        db_table = "fact_ml_scores"


# -----------------------------------
# COMPANY MASTER TABLE
# -----------------------------------

class Company(models.Model):

    symbol = models.CharField(
        max_length=20,
        primary_key=True
    )

    company_name = models.CharField(
        max_length=255
    )

    sector_id = models.IntegerField()

    roe_percentage = models.FloatField(
        null=True
    )

    roce_percentage = models.FloatField(
        null=True
    )

    class Meta:

        managed = False

        db_table = "dim_company"

# -----------------------------------
# SECTOR TABLE
# -----------------------------------

class Sector(models.Model):

    sector_id = models.IntegerField(
        primary_key=True
    )

    sector_name = models.CharField(
        max_length=255
    )

    class Meta:

        managed = False

        db_table = "dim_sector"

class Anomaly(models.Model):

    symbol = models.CharField(
        max_length=20,
        primary_key=True
    )

    year_id = models.IntegerField()

    anomaly_z_any = models.BooleanField()

    anomaly_iso = models.IntegerField()

    final_anomaly = models.BooleanField()

    class Meta:

        managed = False

        db_table = "fact_anomalies"