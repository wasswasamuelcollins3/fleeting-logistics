from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Service(models.Model):
    SERVICE_TYPES = [
        ('cargo', 'Cargo Transport'),
        ('passenger', 'Passenger Transport'),
        ('express', 'Express Delivery'),
        ('warehousing', 'Warehousing'),
        ('customs', 'Customs Clearance'),
    ]

    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='cargo')
    description = models.TextField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_delivery_days = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('arrived_hub', 'Arrived at Hub'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    PRIORITY_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('urgent', 'Urgent'),
    ]

    # Unique tracking ID
    tracking_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    # Shipment details
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField()
    sender_address = models.TextField()

    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    recipient_email = models.EmailField()
    recipient_address = models.TextField()

    # Package details
    package_description = models.TextField()
    weight = models.DecimalField(max_digits=8, decimal_places=2, help_text="Weight in KG")
    dimensions = models.CharField(max_length=50, blank=True, help_text="L x W x H in cm")
    declared_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='standard')

    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Dates
    pickup_date = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)

    # Special instructions
    special_instructions = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_id} - {self.sender_name} to {self.recipient_name}"

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # Generate unique tracking ID
            while True:
                tracking_id = f"FL{uuid.uuid4().hex[:12].upper()}"
                if not Shipment.objects.filter(tracking_id=tracking_id).exists():
                    self.tracking_id = tracking_id
                    break
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class TrackingUpdate(models.Model):
    UPDATE_TYPES = [
        ('status_change', 'Status Change'),
        ('location_update', 'Location Update'),
        ('delay', 'Delay Notice'),
        ('damage', 'Damage Report'),
        ('note', 'General Note'),
    ]

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='tracking_updates')
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPES, default='status_change')
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shipment.tracking_id} - {self.get_update_type_display()}"

    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('shipment_update', 'Shipment Update'),
        ('delivery_reminder', 'Delivery Reminder'),
        ('payment_due', 'Payment Due'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    title = models.CharField(max_length=200)
    message = models.TextField()
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

# Legacy model for backward compatibility
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    estimated_distance = models.FloatField(null=True, blank=True, help_text="Distance in km")
    vehicle_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Rate per km")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.service.name} - {self.date}"

    class Meta:
        ordering = ['-created_at']