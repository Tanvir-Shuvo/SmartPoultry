from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # Dashboard
    # =====================================================

    path(
        "dashboard/",
        views.dashboard_view,
        name="dashboard",
    ),


    # =====================================================
    # Farm Management
    # =====================================================

    path(
        "farms/",
        views.farm_list_view,
        name="farm_list",
    ),

    path(
        "farms/add/",
        views.farm_create_view,
        name="farm_create",
    ),

    path(
        "farms/<int:farm_id>/",
        views.farm_detail_view,
        name="farm_detail",
    ),

    path(
        "farms/<int:farm_id>/edit/",
        views.farm_edit_view,
        name="farm_edit",
    ),

    path(
        "farms/<int:farm_id>/delete/",
        views.farm_delete_view,
        name="farm_delete",
    ),


    # =====================================================
    # Batch Management
    # =====================================================

    path(
        "batches/",
        views.batch_list_view,
        name="batch_list",
    ),

    path(
        "batches/add/",
        views.batch_create_view,
        name="batch_create",
    ),

    path(
        "batches/<int:batch_id>/",
        views.batch_detail_view,
        name="batch_detail",
    ),

    path(
        "batches/<int:batch_id>/edit/",
        views.batch_edit_view,
        name="batch_edit",
    ),

    path(
        "batches/<int:batch_id>/delete/",
        views.batch_delete_view,
        name="batch_delete",
    ),

    path(
        "batches/<int:batch_id>/status/",
        views.batch_toggle_status_view,
        name="batch_toggle_status",
    ),


    # =====================================================
    # Daily Record Management
    # =====================================================

    path(
        "records/",
        views.daily_record_list_view,
        name="daily_record_list",
    ),

    path(
        "batches/<int:batch_id>/daily-records/add/",
        views.daily_record_create_view,
        name="daily_record_create",
    ),

    path(
        "records/<int:record_id>/",
        views.daily_record_detail_view,
        name="daily_record_detail",
    ),

    path(
        "records/<int:record_id>/edit/",
        views.daily_record_edit_view,
        name="daily_record_edit",
    ),

    path(
        "records/<int:record_id>/delete/",
        views.daily_record_delete_view,
        name="daily_record_delete",
    ),


    # =====================================================
    # Egg Production Management
    # =====================================================

    path(
        "egg-productions/",
        views.egg_production_list_view,
        name="egg_production_list",
    ),

    path(
        "batches/<int:batch_id>/egg-production/add/",
        views.egg_production_create_view,
        name="egg_production_create",
    ),

    path(
        "egg-productions/<int:egg_id>/edit/",
        views.egg_production_edit_view,
        name="egg_production_edit",
    ),

    path(
        "egg-productions/<int:egg_id>/delete/",
        views.egg_production_delete_view,
        name="egg_production_delete",
    ),


    # =====================================================
    # Expense Management
    # =====================================================

    path(
        "expenses/",
        views.expense_list_view,
        name="expense_list",
    ),

    path(
        "expenses/add/",
        views.expense_create_view,
        name="expense_create",
    ),

    path(
        "expenses/<int:expense_id>/edit/",
        views.expense_edit_view,
        name="expense_edit",
    ),

    path(
        "expenses/<int:expense_id>/delete/",
        views.expense_delete_view,
        name="expense_delete",
    ),
]