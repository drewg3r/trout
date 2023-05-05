from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from main.models import Station


class RouteEndpointsSelectForm(forms.Form):
    start = forms.ModelChoiceField(queryset=Station.objects.filter(disabled=False))
    destination = forms.ModelChoiceField(queryset=Station.objects.filter(disabled=False))

    def clean(self):
        if self.cleaned_data['start'] == self.cleaned_data['destination']:
            raise ValidationError(_('Start and destination should not be the same station'))
        return super().clean()
