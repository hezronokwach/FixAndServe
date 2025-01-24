from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    choices = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )
    field = models.CharField(max_length=30, blank=False,
                             null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, default='Not provided')
    hours_needed = models.DecimalField(decimal_places=1, max_digits=4, default=1.0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=10, editable=False, default=0.00)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    class Meta:
        ordering = ['-request_date']

    def save(self, *args, **kwargs):
        # Calculate total cost before saving
        self.total_cost = self.service.price_hour * self.hours_needed
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer} - {self.service} ({self.status})"
