from django import forms

TABLE_CHOICES = [
    ("fact_balance_sheet", "Balance Sheet"),
    ("fact_profit_loss", "Profit & Loss"),
    ("fact_cash_flow", "Cash Flow"),
]

class BulkImportForm(forms.Form):

    table_name = forms.ChoiceField(
        choices=TABLE_CHOICES
    )

    csv_file = forms.FileField()