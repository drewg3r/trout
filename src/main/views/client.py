from datetime import datetime

from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView

from main.forms import RouteEndpointsSelectForm
from routing.planner.route_displaying import find_route


class RouteEndpointsSelectView(FormView):
    template_name = 'main/client/route_endpoints_select.html'
    form_class = RouteEndpointsSelectForm
    success_url = reverse_lazy('main:landing')

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'main:route',
            kwargs={
                'start_location': self.form.cleaned_data['start'].id,
                'destination': self.form.cleaned_data['destination'].id,
                'departure_timestamp': int(datetime.timestamp(self.form.cleaned_data['departure_time'])),
            }
        )


class RouteView(TemplateView):
    template_name = 'main/client/route.html'

    def build_route(self):
        return find_route(-1, -1, datetime(2023, 5, 12), dry_run=True)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {'route': self.build_route()}
