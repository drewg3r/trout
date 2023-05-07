from datetime import datetime

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from main.forms import RouteEndpointsSelectForm
from main.models import Station
from routing.planner.route_displaying import find_route


class RouteEndpointsSelectView(FormView):
    template_name = 'main/client/route_endpoints_select.html'
    form_class = RouteEndpointsSelectForm
    success_url = reverse_lazy('main:landing')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             f'start: {form.cleaned_data["start"]}; end:{form.cleaned_data["destination"]}')
        return super().form_valid(form)


class RouteView(TemplateView):
    template_name = 'main/client/route.html'

    def get_context_data(self, **kwargs):
        # route = find_route(1, 2, datetime(2023, 4, 24, 16, 12))
        return super().get_context_data(**kwargs) | {'origin': Station.objects.get(id=1), 'destination': Station.objects.get(id=8)}