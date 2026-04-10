from django.db import models

class Booking(models.Model):
    SERVICE_CHOICES = [
        ('cargo', 'Cargo'),
        ('passenger', 'Passenger'),
    ]
    
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type} - {self.date}"
