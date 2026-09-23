from django.urls import path

from .views import (
    batch_create_view,
    batch_delete_view,
    batch_detail_view,
    batch_edit_view,
    batch_list_view,
    batch_toggle_status_view,
    dashboard_view,
    daily_record_create_view,
    daily_record_delete_view,
    daily_record_detail_view,
    daily_record_edit_view,
    daily_record_list_view,
    farm_create_view,
    farm_delete_view,
    farm_detail_view,
    farm_edit_view,
    farm_list_view,
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

    path(
        "batches/add/",
        batch_create_view,
        name="batch_create",
    ),

    path(
        "batches/",
        batch_list_view,
        name="batch_list",
    ),

    path(
        "batches/<int:batch_id>/",
        batch_detail_view,
        name="batch_detail",
    ),

    path(
        "batches/<int:batch_id>/edit/",
        batch_edit_view,
        name="batch_edit",
    ),

    path(
        "batches/<int:batch_id>/delete/",
        batch_delete_view,
        name="batch_delete",
    ),

    path(
        "batches/<int:batch_id>/status/",
        batch_toggle_status_view,
        name="batch_toggle_status",
    ),

    path(
        "records/",
        daily_record_list_view,
        name="daily_record_list",
    ),

    path(
        "records/<int:record_id>/",
        daily_record_detail_view,
        name="daily_record_detail",
    ),

    path(
        "records/<int:record_id>/edit/",
        daily_record_edit_view,
        name="daily_record_edit",
    ),

    path(
        "records/<int:record_id>/delete/",
        daily_record_delete_view,
        name="daily_record_delete",
    ),

    path(
        "batches/<int:batch_id>/daily-records/add/",
        daily_record_create_view,
        name="daily_record_create",
    ),
]