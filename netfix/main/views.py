from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service

def home(request):
    # Get services with request_count > 0, ordered by most requested
    popular_services = Service.objects.filter(
        request_count__gt=0  # Only get services that have been requested
    ).order_by(
        '-request_count'  # Order by request_count in descending order
    )[:5]  # Limit to top 5
    
    return render(request, "main/home.html", {
        'user': request.user,
        'popular_services': popular_services
    })


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
