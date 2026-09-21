from datetime import date

from django import forms

from .models import Farm


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