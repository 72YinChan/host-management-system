from django.urls import path

from .views import (
    CityListView,
    CityDetailView,
    IDCListView,
    IDCDetailView,
    HostListView,
    HostDetailView,
    host_ping_api,
)


app_name = "host_management"

urlpatterns = [
    path("cities/", CityListView.as_view(), name="city-list"),
    path("cities/<int:pk>/", CityDetailView.as_view(), name="city-detail"),
    path("idcs/", IDCListView.as_view(), name="idc-list"),
    path("idcs/<int:pk>/", IDCDetailView.as_view(), name="idc-detail"),
    path("hosts/", HostListView.as_view(), name="host-list"),
    path("hosts/<int:pk>/", HostDetailView.as_view(), name="host-detail"),
    path("hosts/ping/<int:pk>/", host_ping_api, name="host-ping"),
]
