from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from users.models import Company, Customer, User

from .models import Service
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
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
            return redirect('services_list')
    else:
        form = CreateNewService()
    return render(request, 'services/create.html', {'form': form})

def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    return render(request, 'services/request_service.html', {})
