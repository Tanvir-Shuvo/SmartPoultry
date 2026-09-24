from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BatchForm,
    DailyRecordForm,
    EggProductionForm,
    ExpenseForm,
    FarmForm,
)

from .models import (
    Batch,
    DailyRecord,
    EggProduction,
    Expense,
    Farm,
)


# =========================================================
# Dashboard
# =========================================================

@login_required
def dashboard_view(request):

    user = request.user

    # -----------------------------------------------------
    # Farm & Batch Summary
    # -----------------------------------------------------

    user_farms = Farm.objects.filter(
        owner=user
    )

    user_batches = Batch.objects.filter(
        farm__owner=user
    )

    total_farms = user_farms.count()

    total_batches = user_batches.count()

    active_batches = user_batches.filter(
        is_active=True
    ).count()

    inactive_batches = user_batches.filter(
        is_active=False
    ).count()

    # -----------------------------------------------------
    # Bird Summary
    # -----------------------------------------------------

    total_initial_birds = user_batches.aggregate(
        total=Sum("initial_bird_count")
    )["total"] or 0

    total_dead_birds = DailyRecord.objects.filter(
        batch__farm__owner=user
    ).aggregate(
        total=Sum("dead_count")
    )["total"] or 0

    current_birds = max(
        total_initial_birds - total_dead_birds,
        0
    )

    # -----------------------------------------------------
    # Egg Production
    # -----------------------------------------------------

    total_egg_production = EggProduction.objects.filter(
        batch__farm__owner=user
    ).aggregate(
        total=Sum("egg_count")
    )["total"] or 0

    recent_egg_productions = (
        EggProduction.objects
        .filter(
            batch__farm__owner=user
        )
        .select_related(
            "batch",
            "batch__farm",
        )
        .order_by(
            "-production_date",
            "-id",
        )[:5]
    )

    # -----------------------------------------------------
    # Daily Operations
    # -----------------------------------------------------

    user_daily_records = DailyRecord.objects.filter(
        batch__farm__owner=user
    )

    total_feed = user_daily_records.aggregate(
        total=Sum("feed_amount_kg")
    )["total"] or 0

    total_water = user_daily_records.aggregate(
        total=Sum("water_liters")
    )["total"] or 0

    total_mortality = user_daily_records.aggregate(
        total=Sum("dead_count")
    )["total"] or 0

    total_sick = user_daily_records.aggregate(
        total=Sum("sick_count")
    )["total"] or 0

    recent_daily_records = (
        user_daily_records
        .select_related(
            "batch",
            "batch__farm",
        )
        .order_by(
            "-record_date",
            "-id",
        )[:5]
    )

    # -----------------------------------------------------
    # Expense Summary
    # -----------------------------------------------------

    user_expenses = Expense.objects.filter(
        farm__owner=user
    )

    total_expenses = user_expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    recent_expenses = (
        user_expenses
        .select_related(
            "farm",
            "batch",
        )
        .order_by(
            "-expense_date",
            "-id",
        )[:5]
    )

    # -----------------------------------------------------
    # Sales
    # -----------------------------------------------------
    # Sales management has not been implemented yet.
    # These values will be connected after Sale CRUD
    # and financial calculations are completed.

    total_sales = 0
    profit_loss = 0

    # -----------------------------------------------------
    # Farms
    # -----------------------------------------------------

    farms = user_farms.order_by(
        "name"
    )

    # -----------------------------------------------------
    # Dashboard Context
    # -----------------------------------------------------

    context = {
        # Farm & Batch
        "total_farms": total_farms,
        "total_batches": total_batches,
        "active_batches": active_batches,
        "inactive_batches": inactive_batches,

        # Birds
        "current_birds": current_birds,

        # Egg Production
        "total_egg_production": total_egg_production,
        "recent_egg_productions": recent_egg_productions,

        # Operations
        "total_feed": total_feed,
        "total_water": total_water,
        "total_mortality": total_mortality,
        "total_sick": total_sick,
        "recent_daily_records": recent_daily_records,

        # Expenses
        "total_expenses": total_expenses,
        "recent_expenses": recent_expenses,

        # Finance
        "total_sales": total_sales,
        "profit_loss": profit_loss,

        # Farms
        "farms": farms,
    }

    return render(
        request,
        "poultry/dashboard.html",
        context,
    )


# =========================================================
# Farm Management
# =========================================================

@login_required
def farm_list_view(request):

    farms = Farm.objects.filter(
        owner=request.user
    ).order_by("name")

    return render(
        request,
        "poultry/farm_list.html",
        {
            "farms": farms,
        }
    )


@login_required
def farm_create_view(request):

    if request.method == "POST":

        form = FarmForm(
            request.POST
        )

        if form.is_valid():

            farm = form.save(
                commit=False
            )

            farm.owner = request.user
            farm.save()

            return redirect(
                "farm_list"
            )

    else:

        form = FarmForm()

    return render(
        request,
        "poultry/farm_form.html",
        {
            "form": form,
            "page_title": "Add Farm",
        }
    )


@login_required
def farm_detail_view(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        owner=request.user,
    )

    batches = farm.batches.all().order_by(
        "-start_date",
        "-id",
    )

    return render(
        request,
        "poultry/farm_detail.html",
        {
            "farm": farm,
            "batches": batches,
        }
    )


@login_required
def farm_edit_view(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        owner=request.user,
    )

    if request.method == "POST":

        form = FarmForm(
            request.POST,
            instance=farm,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "farm_detail",
                farm_id=farm.id,
            )

    else:

        form = FarmForm(
            instance=farm
        )

    return render(
        request,
        "poultry/farm_form.html",
        {
            "form": form,
            "farm": farm,
            "page_title": "Edit Farm",
        }
    )


@login_required
def farm_delete_view(request, farm_id):

    farm = get_object_or_404(
        Farm,
        id=farm_id,
        owner=request.user,
    )

    if request.method == "POST":

        farm.delete()

        return redirect(
            "farm_list"
        )

    return render(
        request,
        "poultry/farm_confirm_delete.html",
        {
            "farm": farm,
        }
    )


# =========================================================
# Batch Management
# =========================================================

@login_required
def batch_list_view(request):

    batches = (
        Batch.objects
        .filter(
            farm__owner=request.user
        )
        .select_related("farm")
        .order_by(
            "-start_date",
            "-id",
        )
    )

    return render(
        request,
        "poultry/batch_list.html",
        {
            "batches": batches,
        }
    )


@login_required
def batch_create_view(request):

    if request.method == "POST":

        form = BatchForm(
            request.POST
        )

        form.fields["farm"].queryset = Farm.objects.filter(
            owner=request.user
        )

        if form.is_valid():

            batch = form.save()

            return redirect(
                "batch_detail",
                batch_id=batch.id,
            )

    else:

        form = BatchForm()

        form.fields["farm"].queryset = Farm.objects.filter(
            owner=request.user
        )

    return render(
        request,
        "poultry/batch_form.html",
        {
            "form": form,
            "page_title": "Add Batch",
        }
    )


@login_required
def batch_detail_view(request, batch_id):

    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    daily_records = (
        batch.daily_records
        .order_by(
            "-record_date",
            "-id",
        )
    )

    egg_productions = (
        batch.egg_productions
        .order_by(
            "-production_date",
            "-id",
        )
    )

    return render(
        request,
        "poultry/batch_detail.html",
        {
            "batch": batch,
            "daily_records": daily_records,
            "egg_productions": egg_productions,
        }
    )


@login_required
def batch_edit_view(request, batch_id):

    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        form = BatchForm(
            request.POST,
            instance=batch,
        )

        form.fields["farm"].queryset = Farm.objects.filter(
            owner=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                "batch_detail",
                batch_id=batch.id,
            )

    else:

        form = BatchForm(
            instance=batch
        )

        form.fields["farm"].queryset = Farm.objects.filter(
            owner=request.user
        )

    return render(
        request,
        "poultry/batch_form.html",
        {
            "form": form,
            "batch": batch,
            "page_title": "Edit Batch",
        }
    )


@login_required
def batch_delete_view(request, batch_id):

    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        farm_id = batch.farm_id

        batch.delete()

        return redirect(
            "farm_detail",
            farm_id=farm_id,
        )

    return render(
        request,
        "poultry/batch_confirm_delete.html",
        {
            "batch": batch,
        }
    )


@login_required
def batch_toggle_status_view(request, batch_id):

    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        batch.is_active = not batch.is_active

        batch.save(
            update_fields=["is_active"]
        )

    return redirect(
        "batch_detail",
        batch_id=batch.id,
    )


# =========================================================
# Daily Record Management
# =========================================================

@login_required
def daily_record_list_view(request):

    records = (
        DailyRecord.objects
        .filter(
            batch__farm__owner=request.user
        )
        .select_related(
            "batch",
            "batch__farm",
        )
        .order_by(
            "-record_date",
            "-id",
        )
    )

    return render(
        request,
        "poultry/daily_record_list.html",
        {
            "records": records,
        }
    )


@login_required
def daily_record_create_view(request, batch_id):

    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        form = DailyRecordForm(
            request.POST
        )

        if form.is_valid():

            record = form.save(
                commit=False
            )

            record.batch = batch
            record.save()

            return redirect(
                "batch_detail",
                batch_id=batch.id,
            )

    else:

        form = DailyRecordForm()

    return render(
        request,
        "poultry/daily_record_form.html",
        {
            "form": form,
            "batch": batch,
            "page_title": "Add Daily Record",
        }
    )


@login_required
def daily_record_detail_view(request, record_id):

    record = get_object_or_404(
        DailyRecord,
        id=record_id,
        batch__farm__owner=request.user,
    )

    return render(
        request,
        "poultry/daily_record_detail.html",
        {
            "record": record,
        }
    )


@login_required
def daily_record_edit_view(request, record_id):

    record = get_object_or_404(
        DailyRecord,
        id=record_id,
        batch__farm__owner=request.user,
    )

    if request.method == "POST":

        form = DailyRecordForm(
            request.POST,
            instance=record,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "daily_record_detail",
                record_id=record.id,
            )

    else:

        form = DailyRecordForm(
            instance=record
        )

    return render(
        request,
        "poultry/daily_record_form.html",
        {
            "form": form,
            "record": record,
            "batch": record.batch,
            "page_title": "Edit Daily Record",
        }
    )


@login_required
def daily_record_delete_view(request, record_id):

    record = get_object_or_404(
        DailyRecord,
        id=record_id,
        batch__farm__owner=request.user,
    )

    if request.method == "POST":

        batch_id = record.batch_id

        record.delete()

        return redirect(
            "batch_detail",
            batch_id=batch_id,
        )

    return render(
        request,
        "poultry/daily_record_confirm_delete.html",
        {
            "record": record,
        }
    )


# =========================================================
# Egg Production Management
# =========================================================

@login_required
def egg_production_list_view(request):

    egg_productions = (
        EggProduction.objects
        .filter(
            batch__farm__owner=request.user
        )
        .select_related(
            "batch",
            "batch__farm",
        )
        .order_by(
            "-production_date",
            "-id",
        )
    )

    return render(
        request,
        "poultry/egg_production_list.html",
        {
            "egg_productions": egg_productions,
        }
    )


@login_required
def egg_production_create_view(request, batch_id):

    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        form = EggProductionForm(
            request.POST
        )

        if form.is_valid():

            egg_production = form.save(
                commit=False
            )

            egg_production.batch = batch
            egg_production.save()

            return redirect(
                "batch_detail",
                batch_id=batch.id,
            )

    else:

        form = EggProductionForm()

    return render(
        request,
        "poultry/egg_production_form.html",
        {
            "form": form,
            "batch": batch,
            "page_title": "Add Egg Production",
        }
    )


@login_required
def egg_production_edit_view(request, egg_id):

    egg_production = get_object_or_404(
        EggProduction,
        id=egg_id,
        batch__farm__owner=request.user,
    )

    if request.method == "POST":

        form = EggProductionForm(
            request.POST,
            instance=egg_production,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "batch_detail",
                batch_id=egg_production.batch_id,
            )

    else:

        form = EggProductionForm(
            instance=egg_production
        )

    return render(
        request,
        "poultry/egg_production_form.html",
        {
            "form": form,
            "egg_production": egg_production,
            "batch": egg_production.batch,
            "page_title": "Edit Egg Production",
        }
    )


@login_required
def egg_production_delete_view(request, egg_id):

    egg_production = get_object_or_404(
        EggProduction,
        id=egg_id,
        batch__farm__owner=request.user,
    )

    if request.method == "POST":

        batch_id = egg_production.batch_id

        egg_production.delete()

        return redirect(
            "batch_detail",
            batch_id=batch_id,
        )

    return render(
        request,
        "poultry/egg_production_confirm_delete.html",
        {
            "egg_production": egg_production,
        }
    )


# =========================================================
# Expense Management
# =========================================================

@login_required
def expense_list_view(request):

    expenses = (
        Expense.objects
        .filter(
            farm__owner=request.user
        )
        .select_related(
            "farm",
            "batch",
        )
        .order_by(
            "-expense_date",
            "-id",
        )
    )

    total_expenses = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "poultry/expense_list.html",
        {
            "expenses": expenses,
            "total_expenses": total_expenses,
        },
    )


@login_required
def expense_create_view(request):

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "expense_list"
            )

    else:

        form = ExpenseForm(
            user=request.user
        )

    return render(
        request,
        "poultry/expense_form.html",
        {
            "form": form,
            "page_title": "Add Expense",
        }
    )


@login_required
def expense_edit_view(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "expense_list"
            )

    else:

        form = ExpenseForm(
            instance=expense,
            user=request.user,
        )

    return render(
        request,
        "poultry/expense_form.html",
        {
            "form": form,
            "page_title": "Edit Expense",
            "expense": expense,
        }
    )


@login_required
def expense_delete_view(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        farm__owner=request.user,
    )

    if request.method == "POST":

        expense.delete()

        return redirect(
            "expense_list"
        )

    return render(
        request,
        "poultry/expense_confirm_delete.html",
        {
            "expense": expense,
        }
    )