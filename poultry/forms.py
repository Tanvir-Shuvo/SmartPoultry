from datetime import date

from django import forms

from .models import (
    Farm,
    Batch,
    DailyRecord,
    EggProduction,
    Expense,
)


class FarmForm(forms.ModelForm):

    class Meta:
        model = Farm
        fields = [
            "name",
            "location",
            "farm_type",
            "capacity",
            "start_date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_date"].initial = date.today()


class BatchForm(forms.ModelForm):

    class Meta:
        model = Batch
        fields = [
            "farm",
            "code",
            "poultry_type",
            "start_date",
            "initial_bird_count",
            "purchase_price_per_bird",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_date"].initial = date.today()


class DailyRecordForm(forms.ModelForm):

    class Meta:
        model = DailyRecord
        fields = [
            "record_date",
            "feed_amount_kg",
            "water_liters",
            "dead_count",
            "sick_count",
            "medicine_used",
            "medicine_quantity",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["record_date"].initial = date.today()


class EggProductionForm(forms.ModelForm):

    class Meta:
        model = EggProduction
        fields = [
            "production_date",
            "egg_count",
            "damaged_egg_count",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["production_date"].initial = date.today()


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = [
            "farm",
            "batch",
            "expense_type",
            "category",
            "amount",
            "expense_date",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["expense_date"].initial = date.today()

        if user is not None:
            self.fields["farm"].queryset = Farm.objects.filter(
                owner=user
            )

            self.fields["batch"].queryset = Batch.objects.filter(
                farm__owner=user
            )

        else:
            self.fields["farm"].queryset = Farm.objects.none()
            self.fields["batch"].queryset = Batch.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        farm = cleaned_data.get("farm")
        batch = cleaned_data.get("batch")
        expense_type = cleaned_data.get("expense_type")
        amount = cleaned_data.get("amount")

        if amount is not None and amount <= 0:
            self.add_error(
                "amount",
                "Amount must be greater than zero.",
            )

        if expense_type == "FARM":
            if batch is not None:
                self.add_error(
                    "batch",
                    "Farm expense should not be linked to a batch.",
                )

        elif expense_type == "BATCH":
            if batch is None:
                self.add_error(
                    "batch",
                    "Please select a batch for a batch expense.",
                )

        if farm is not None and batch is not None:
            if batch.farm_id != farm.id:
                self.add_error(
                    "batch",
                    "Selected batch does not belong to the selected farm.",
                )

        return cleaned_data