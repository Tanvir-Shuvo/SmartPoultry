
from datetime import date

from django import forms

from .models import Farm, Batch, DailyRecord


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