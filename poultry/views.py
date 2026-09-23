from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BatchForm, DailyRecordForm, FarmForm
from .models import Batch, DailyRecord, Farm


@login_required
def dashboard_view(request):
    total_farms = Farm.objects.filter(
        owner=request.user
    ).count()

    total_batches = Batch.objects.filter(
        farm__owner=request.user
    ).count()

    active_batches = Batch.objects.filter(
        farm__owner=request.user,
        is_active=True,
    ).count()

    inactive_batches = Batch.objects.filter(
        farm__owner=request.user,
        is_active=False,
    ).count()

    current_birds = Batch.objects.filter(
        farm__owner=request.user,
        is_active=True,
    ).aggregate(
        total=Sum("initial_bird_count")
    )["total"] or 0

    farms = Farm.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "poultry/dashboard.html",
        {
            "total_farms": total_farms,
            "total_batches": total_batches,
            "active_batches": active_batches,
            "inactive_batches": inactive_batches,
            "current_birds": current_birds,
            "farms": farms,
        },
    )


@login_required
def farm_create_view(request):
    if request.method == "POST":
        form = FarmForm(request.POST)

        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()

            return redirect("dashboard")

    else:
        form = FarmForm()

    return render(
        request,
        "poultry/farm_form.html",
        {
            "form": form,
        },
    )


@login_required
def farm_list_view(request):
    farms = Farm.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "poultry/farm_list.html",
        {
            "farms": farms,
        },
    )


@login_required
def farm_detail_view(request, farm_id):
    farm = get_object_or_404(
        Farm,
        id=farm_id,
        owner=request.user,
    )

    batches = Batch.objects.filter(
        farm=farm
    )

    return render(
        request,
        "poultry/farm_detail.html",
        {
            "farm": farm,
            "batches": batches,
        },
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
            instance=farm,
        )

    return render(
        request,
        "poultry/farm_form.html",
        {
            "form": form,
            "farm": farm,
        },
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

        return redirect("farm_list")

    return render(
        request,
        "poultry/farm_confirm_delete.html",
        {
            "farm": farm,
        },
    )


@login_required
def batch_create_view(request):
    if request.method == "POST":
        form = BatchForm(request.POST)

        form.fields["farm"].queryset = Farm.objects.filter(
            owner=request.user
        )

        if form.is_valid():
            form.save()

            return redirect("dashboard")

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
        },
    )


@login_required
def batch_list_view(request):
    batches = Batch.objects.filter(
        farm__owner=request.user
    )

    status = request.GET.get("status")

    if status == "active":
        batches = batches.filter(
            is_active=True
        )

    elif status == "inactive":
        batches = batches.filter(
            is_active=False
        )

    return render(
        request,
        "poultry/batch_list.html",
        {
            "batches": batches,
            "status": status,
        },
    )


@login_required
def batch_detail_view(request, batch_id):
    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    daily_records = DailyRecord.objects.filter(
        batch=batch
    ).order_by(
        "-record_date",
        "-id",
    )

    return render(
        request,
        "poultry/batch_detail.html",
        {
            "batch": batch,
            "daily_records": daily_records,
        },
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
            instance=batch,
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
        },
    )


@login_required
def batch_delete_view(request, batch_id):
    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":
        batch.delete()

        return redirect("batch_list")

    return render(
        request,
        "poultry/batch_delete.html",
        {
            "batch": batch,
        },
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


@login_required
def daily_record_list_view(request):
    daily_records = DailyRecord.objects.filter(
        batch__farm__owner=request.user
    ).select_related(
        "batch",
        "batch__farm",
    ).order_by(
        "-record_date",
        "-id",
    )

    return render(
        request,
        "poultry/daily_record_list.html",
        {
            "daily_records": daily_records,
        },
    )


@login_required
def daily_record_create_view(request, batch_id):
    batch = get_object_or_404(
        Batch,
        id=batch_id,
        farm__owner=request.user,
    )

    if request.method == "POST":
        form = DailyRecordForm(request.POST)

        if form.is_valid():
            daily_record = form.save(commit=False)
            daily_record.batch = batch
            daily_record.save()

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
        },
    )


@login_required
def daily_record_detail_view(request, record_id):
    daily_record = get_object_or_404(
        DailyRecord,
        id=record_id,
        batch__farm__owner=request.user,
    )

    return render(
        request,
        "poultry/daily_record_detail.html",
        {
            "daily_record": daily_record,
        },
    )


@login_required
def daily_record_edit_view(request, record_id):
    daily_record = get_object_or_404(
        DailyRecord,
        id=record_id,
        batch__farm__owner=request.user,
    )

    if request.method == "POST":
        form = DailyRecordForm(
            request.POST,
            instance=daily_record,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "daily_record_detail",
                record_id=daily_record.id,
            )

    else:
        form = DailyRecordForm(
            instance=daily_record,
        )

    return render(
        request,
        "poultry/daily_record_form.html",
        {
            "form": form,
            "batch": daily_record.batch,
            "daily_record": daily_record,
        },
    )


@login_required
def daily_record_delete_view(request, record_id):
    daily_record = get_object_or_404(
        DailyRecord,
        id=record_id,
        batch__farm__owner=request.user,
    )

    if request.method == "POST":
        batch_id = daily_record.batch.id

        daily_record.delete()

        return redirect(
            "batch_detail",
            batch_id=batch_id,
        )

    return render(
        request,
        "poultry/daily_record_confirm_delete.html",
        {
            "daily_record": daily_record,
        },
    )