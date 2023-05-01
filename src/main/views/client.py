from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from main.forms import RouteEndpointsSelectForm


class RouteEndpointsSelectView(FormView):
    template_name = 'main/client/route_endpoints_select.html'
    form_class = RouteEndpointsSelectForm
    success_url = reverse_lazy('main:landing')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, f'start: {form.cleaned_data["start"]}; end:{form.cleaned_data["destination"]}')
        return super().form_valid(form)
