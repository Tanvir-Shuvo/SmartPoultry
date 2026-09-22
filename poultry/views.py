
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FarmForm, BatchForm
from .models import Farm, Batch


@login_required
def dashboard_view(request):
    total_farms = Farm.objects.filter(
        owner=request.user
    ).count()

    active_batches = Batch.objects.filter(
        farm__owner=request.user,
        is_active=True,
    ).count()

    farms = Farm.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "poultry/dashboard.html",
        {
            "total_farms": total_farms,
            "active_batches": active_batches,
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
