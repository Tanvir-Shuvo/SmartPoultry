from django.urls import path

from .views import dashboard_view, farm_create_view


urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("farms/add/", farm_create_view, name="farm_create"),
]