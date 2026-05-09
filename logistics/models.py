from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    # Profile verification
    verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # Profile picture
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.role}"


class Shipment(models.Model):
    """Main shipment/booking model for cargo transportation"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('hub_arrival', 'Arrived at Hub'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    VEHICLE_CHOICES = (
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('cargo', 'Cargo Truck'),
        ('bus', 'Bus'),
    )
    
    VEHICLE_RATES = {
        'car': 2000,
        'van': 2500,
        'truck': 4000,
        'cargo': 5500,
        'bus': 3500,
    }
    
    # Tracking
    tracking_id = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Customer
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments')
    
    # Shipment Details
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField(blank=True)
    
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_email = models.EmailField(blank=True)
    
    description = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    
    # Vehicle
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    current_location = models.CharField(max_length=255, blank=True)
    
    # Dates
    pickup_date = models.DateTimeField()
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    
    # Pricing
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=20,
        choices=(('cash', 'Cash'), ('card', 'Card'), ('mobile_money', 'Mobile Money')),
        default='cash'
    )
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_id']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['pickup_date']),
        ]
    
    def __str__(self):
        return f"{self.tracking_id} - {self.receiver_name}"
    
    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # Generate unique tracking ID
            self.tracking_id = f"TRK{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)


class TrackingUpdate(models.Model):
    """Real-time tracking updates for shipments"""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='updates')
    
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    message = models.TextField()
    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Tracking Updates'
    
    def __str__(self):
        return f"{self.shipment.tracking_id} - {self.status} - {self.timestamp}"


class Notification(models.Model):
    """User notifications for shipment updates"""
    NOTIFICATION_TYPES = (
        ('shipment_created', 'Shipment Created'),
        ('shipment_confirmed', 'Shipment Confirmed'),
        ('shipment_picked_up', 'Shipment Picked Up'),
        ('shipment_in_transit', 'Shipment In Transit'),
        ('shipment_delivered', 'Shipment Delivered'),
        ('shipment_cancelled', 'Shipment Cancelled'),
        ('payment_reminder', 'Payment Reminder'),
        ('system_alert', 'System Alert'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    
    # Notification channels
    send_email = models.BooleanField(default=True)
    send_sms = models.BooleanField(default=False)
    send_whatsapp = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    is_replied = models.BooleanField(default=False)
    reply_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Booking(models.Model):
    """Legacy booking model - kept for backward compatibility"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.service.name} - {self.date}"
