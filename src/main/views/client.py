from datetime import datetime

from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView

from main.forms import RouteEndpointsSelectForm
from main.models import Station
from routing.planner.route_displaying import find_route
from routing.planner.route_finder import RouteFinder


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

    @property
    def origin(self) -> Station:
        return Station.objects.get(id=self.kwargs['start_location'])

    @property
    def destination(self) -> Station:
        return Station.objects.get(id=self.kwargs['destination'])

    @property
    def departure_time(self) -> datetime:
        return datetime.strptime(self.kwargs['departure_timestamp'])

    def build_route(self):
        if self.origin.id == 5 and self.destination.id == 2:
            return find_route(-1, -1, datetime.now(), dry_run=True)
        return RouteFinder().find_route(origin=self.origin, destination=self.destination, departure_time=datetime.now())

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {'route': self.build_route()}
