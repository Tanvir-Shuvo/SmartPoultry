from django.urls import path

from .views import (
    dashboard_view,
    farm_create_view,
    farm_list_view,
    farm_detail_view,
    farm_edit_view,
    farm_delete_view,
)


urlpatterns = [
    path(
        "dashboard/",
        dashboard_view,
        name="dashboard",
    ),

    path(
        "farms/add/",
        farm_create_view,
        name="farm_create",
    ),

    path(
        "farms/",
        farm_list_view,
        name="farm_list",
    ),

    path(
        "farms/<int:farm_id>/",
        farm_detail_view,
        name="farm_detail",
    ),

    path(
        "farms/<int:farm_id>/edit/",
        farm_edit_view,
        name="farm_edit",
    ),

    path(
        "farms/<int:farm_id>/delete/",
        farm_delete_view,
        name="farm_delete",
    ),
]