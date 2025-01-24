from django.shortcuts import render
from datetime import date

from users.models import User, Company
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    # fetches the customer user
    user = User.objects.get(username=name)
    customer = user.customer
    
    # Calculate age from birth date
    today = date.today()
    birth_date = customer.birth
    user_age = None
    if birth_date:
        user_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # Get customer's requested services
    service_history = ServiceRequest.objects.filter(customer=customer).select_related('service', 'service__company', 'service__company__user')
    
    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': user_age,
        'sh': service_history  # Using 'sh' to match existing template
    })


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', 
    {'user': user, 
    'services': services
    })
