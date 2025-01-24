from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import logging
from django.conf import settings  # Add this import
from django.contrib import messages

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from users.models import Company, Customer, User

from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    logger.debug("Entering service_list view")
    
    try:
        services = Service.objects.all().order_by('-date')
        logger.debug(f"Found {services.count()} total services")
        
        # Log each service for debugging
        for service in services:
            logger.debug(f"Service: {service.name} (ID: {service.id})")
            
        paginator = Paginator(services, 9)
        page = request.GET.get('page')
        services = paginator.get_page(page)
        
        context = {
            'services': services,
            'debug': True  # Simplified debug flag
        }
        
        return render(request, 'services/list.html', context)
        
    except Exception as e:
        logger.error(f"Error in service_list: {str(e)}")
        logger.exception("Full traceback:")
        raise


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    logger.debug("Entering create service view")
    if request.method == 'POST':
        form = CreateNewService(request.POST)
        company = request.user.company
        if form.is_valid():
            if company.field != 'All in One' and company.field != form.cleaned_data['field']:
                form.add_error('field', 'You can only create services in your field of work.')
                return render(request, 'services/create.html', {'form': form})
            
            service = Service(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
            )
            service.save()
            return redirect('service_list')
    else:
        form = CreateNewService()
    return render(request, 'services/create.html', {'form': form})

def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


@login_required
def request_service(request, id):
    if not hasattr(request.user, 'customer'):
        messages.error(request, "Only customers can request services")
        return redirect('service_list')
    
    try:
        service = Service.objects.get(id=id)
        
        if request.method == 'POST':
            form = RequestServiceForm(request.POST)
            if form.is_valid():
                # Create service request
                ServiceRequest.objects.create(
                    service=service,
                    customer=request.user.customer,
                    address=form.cleaned_data['address'],
                    hours_needed=form.cleaned_data['hours_needed']
                )
                
                # Increment request count
                service.request_count += 1
                service.save()
                
                messages.success(request, f"Service request for {service.name} has been submitted")
                return redirect('service_list')
        else:
            form = RequestServiceForm()
        
        return render(request, 'services/request_service.html', {
            'form': form,
            'service': service
        })
        
    except Service.DoesNotExist:
        messages.error(request, "Service not found")
        return redirect('service_list')
    except Exception as e:
        logger.error(f"Error in request_service: {str(e)}")
        messages.error(request, "An error occurred while processing your request")
        return redirect('service_list')
