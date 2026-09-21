from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Farm
from .forms import FarmForm


def home(request):
    return render(request, "poultry/home.html")


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
        {"form": form},
    )