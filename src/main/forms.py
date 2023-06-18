from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from main.models import Station


class FakeRelation:
    def __init__(self, model):
        self.model = model


class CustomAutocompleteSelect(AutocompleteSelect):
    def __init__(self, model, admin_site):
        rel = FakeRelation(model)
        super().__init__(rel, admin_site)


class RouteEndpointsSelectForm(forms.Form):
    start = forms.ModelChoiceField(queryset=Station.objects.filter(disabled=False))
    destination = forms.ModelChoiceField(queryset=Station.objects.filter(disabled=False))
    departure_time = forms.DateTimeField()

    def clean(self):
        if self.cleaned_data['start'] == self.cleaned_data['destination']:
            raise ValidationError(_('Start and destination should not be the same station'))
        return super().clean()
