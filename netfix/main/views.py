from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service


def home(request):
    # Get the most requested services
    popular_services = Service.objects.order_by('-request_count')[:5]
    return render(request, "main/home.html", {
        'user': request.user,
        'popular_services': popular_services
    })


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
