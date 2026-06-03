from django.db import models


class Company(models.Model):

    id = models.TextField(
        primary_key=True
    )

    company_logo = models.TextField(
        blank=True,
        null=True
    )

    company_name = models.TextField(
        blank=True,
        null=True
    )

    symbol = models.TextField(
        blank=True,
        null=True
    )

    sector_id = models.IntegerField(
        blank=True,
        null=True
    )

    roe_percentage = models.FloatField(
        blank=True,
        null=True
    )

    roce_percentage = models.FloatField(
        blank=True,
        null=True
    )

    about_company = models.TextField(
        blank=True,
        null=True
    )

    website = models.TextField(
        blank=True,
        null=True
    )

    chart_link = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        managed = False

        db_table = "dim_company"

    def __str__(self):

        return str(self.company_name)
    
class BalanceSheet(models.Model):

    id = models.BigIntegerField(
        primary_key=True
    )

    symbol = models.TextField()

    year = models.BigIntegerField()

    equity_capital = models.FloatField()

    reserves = models.BigIntegerField()

    borrowings = models.BigIntegerField()

    other_liabilities = models.BigIntegerField()

    total_liabilities = models.BigIntegerField()

    fixed_assets = models.BigIntegerField()

    cwip = models.BigIntegerField()

    investments = models.BigIntegerField()

    other_asset = models.BigIntegerField()

    total_assets = models.BigIntegerField()

    date = models.TextField()

    month = models.BigIntegerField()

    year_id = models.BigIntegerField()

    de_ratio = models.FloatField()

    class Meta:

        managed = False

        db_table = "fact_balance_sheet"

class ProfitLoss(models.Model):

    id = models.BigIntegerField(
        primary_key=True
    )

    symbol = models.TextField()

    year = models.BigIntegerField()

    sales = models.BigIntegerField()

    expenses = models.BigIntegerField()

    operating_profit = models.FloatField()

    opm_percentage = models.FloatField()

    other_income = models.BigIntegerField()

    interest = models.BigIntegerField()

    depreciation = models.BigIntegerField()

    profit_before_tax = models.BigIntegerField()

    tax_percentage = models.FloatField()

    net_profit = models.BigIntegerField()

    eps = models.FloatField()

    dividend_payout = models.FloatField()

    date = models.TextField()

    month = models.BigIntegerField()

    year_id = models.IntegerField()

    opm_pct = models.FloatField()

    profit_margin = models.FloatField()

    class Meta:

        managed = False

        db_table = "fact_profit_loss"