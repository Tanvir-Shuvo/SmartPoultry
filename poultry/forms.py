from datetime import date

from django import forms

from .models import Farm, Batch


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