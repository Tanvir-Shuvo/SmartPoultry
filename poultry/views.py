from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FarmForm
from .models import Farm


@login_required
def dashboard_view(request):
    total_farms = Farm.objects.filter(
        owner=request.user
    ).count()

    return render(
        request,
        "poultry/dashboard.html",
        {
            "total_farms": total_farms,
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

    return render(
        request,
        "poultry/farm_detail.html",
        {
            "farm": farm,
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