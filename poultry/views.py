from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Farm


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