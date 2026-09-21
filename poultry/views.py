from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, "poultry/home.html")


@login_required
def dashboard_view(request):
    return render(request, "poultry/dashboard.html")