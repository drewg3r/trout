from django.urls import path
from django.views.generic import TemplateView

from main.views.client import RouteEndpointsSelectView, RouteView

app_name = 'main'

urlpatterns = [
    path('', TemplateView.as_view(template_name="main/landing.html"), name='landing'),
    path('route_endpoints_select', RouteEndpointsSelectView.as_view(), name='route_endpoints_select'),
    path('route/from/<int:start_location>/to/<int:destination>/departure_time/<int:departure_timestamp>', RouteView.as_view(), name='route'),
]
