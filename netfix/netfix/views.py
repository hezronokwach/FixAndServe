from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from users.models import User, Company
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


@login_required
def customer_profile(request, name):
    try:
        # fetches the customer user
        user = User.objects.get(username=name)
        if not user.is_customer:
            raise Http404("User is not a customer")
            
        # Only allow viewing own profile unless staff/admin
        if user != request.user and not request.user.is_staff:
            messages.error(request, "You don't have permission to view this profile")
            return redirect('main:home')
            
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
    except User.DoesNotExist:
        raise Http404("User does not exist")


def company_profile(request, name):
    """Public view - anyone can see company profiles"""
    try:
        # fetches the company user and all of the services available by it
        user = get_object_or_404(User, username=name)
        if not user.is_company:
            raise Http404("User is not a company")
            
        services = Service.objects.filter(
            company=Company.objects.get(user=user)).order_by("-date")

        return render(request, 'users/profile.html', 
        {'user': user, 
        'services': services
        })
    except User.DoesNotExist:
        raise Http404("User does not exist")
