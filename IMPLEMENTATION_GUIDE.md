# Fleeting Logistics - Implementation Guide

## Quick Start

### Step 1: Update Base Template
Add these CSS files to your `base.html` head:
```html
<link href="{% static 'css/modern.css' %}" rel="stylesheet">
<link href="{% static 'css/navbar-footer.css' %}" rel="stylesheet">
```

### Step 2: Create New Authentication System

#### Models to Update (`logistics/models.py`)
```python
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shipment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('hub_arrival', 'Arrived at Hub'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    tracking_id = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Details
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    # Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    current_location = models.CharField(max_length=255)
    
    # Dates
    pickup_date = models.DateTimeField()
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    
    # Cost
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tracking_id} - {self.status}"

class TrackingUpdate(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Step 3: Create New Views

#### Dashboard View (`logistics/views.py`)
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Shipment, Notification

@login_required
def dashboard(request):
    shipments = Shipment.objects.filter(customer=request.user).order_by('-created_at')[:10]
    recent_shipments = shipments[:5]
    total_shipments = Shipment.objects.filter(customer=request.user).count()
    delivered = Shipment.objects.filter(customer=request.user, status='delivered').count()
    pending = Shipment.objects.filter(customer=request.user, status__in=['pending', 'picked_up', 'in_transit']).count()
    
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    
    context = {
        'shipments': recent_shipments,
        'total_shipments': total_shipments,
        'delivered': delivered,
        'pending': pending,
        'notifications': notifications,
    }
    return render(request, 'dashboard.html', context)

@login_required
def shipment_detail(request, tracking_id):
    shipment = Shipment.objects.get(tracking_id=tracking_id)
    updates = shipment.updates.all().order_by('-timestamp')
    
    context = {
        'shipment': shipment,
        'updates': updates,
    }
    return render(request, 'shipment_detail.html', context)
```

### Step 4: Create Templates

#### Dashboard Template (`templates/dashboard.html`)
```html
{% extends 'base.html' %}

{% block title %}Dashboard - Fleeting Logistics{% endblock %}

{% block content %}
<div class="container py-5">
    <h1>Welcome, {{ user.first_name|default:user.username }}!</h1>
    
    <!-- Stats Cards -->
    <div class="grid grid-3 mb-5">
        <div class="card">
            <div class="flex-between">
                <div>
                    <p class="text-secondary mb-1">Total Shipments</p>
                    <h3 class="mb-0">{{ total_shipments }}</h3>
                </div>
                <i class="fas fa-box text-primary" style="font-size: 2.5rem; opacity: 0.2;"></i>
            </div>
        </div>
        
        <div class="card">
            <div class="flex-between">
                <div>
                    <p class="text-secondary mb-1">Delivered</p>
                    <h3 class="text-success mb-0">{{ delivered }}</h3>
                </div>
                <i class="fas fa-check-circle text-success" style="font-size: 2.5rem; opacity: 0.2;"></i>
            </div>
        </div>
        
        <div class="card">
            <div class="flex-between">
                <div>
                    <p class="text-secondary mb-1">In Progress</p>
                    <h3 class="text-primary mb-0">{{ pending }}</h3>
                </div>
                <i class="fas fa-truck text-primary" style="font-size: 2.5rem; opacity: 0.2;"></i>
            </div>
        </div>
    </div>
    
    <!-- Recent Shipments -->
    <div class="card mb-5">
        <div class="card-header">
            <h4 class="card-title">Recent Shipments</h4>
        </div>
        <div class="card-body">
            {% if shipments %}
                <table class="table">
                    <thead>
                        <tr>
                            <th>Tracking ID</th>
                            <th>Destination</th>
                            <th>Status</th>
                            <th>Delivery</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for shipment in shipments %}
                            <tr>
                                <td><code>{{ shipment.tracking_id }}</code></td>
                                <td>{{ shipment.destination }}</td>
                                <td><span class="badge badge-{{ shipment.status }}">{{ shipment.get_status_display }}</span></td>
                                <td>{{ shipment.estimated_delivery|date:"M d, Y" }}</td>
                                <td>
                                    <a href="{% url 'shipment_detail' shipment.tracking_id %}" class="btn btn-sm btn-primary">
                                        Track
                                    </a>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <p class="text-secondary">No shipments yet.</p>
                <a href="{% url 'booking' %}" class="btn btn-primary">Create Shipment</a>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### Step 5: Update URLs

#### Add to `fleeting_logistics/urls.py`
```python
path('dashboard/', views.dashboard, name='dashboard'),
path('shipment/<str:tracking_id>/', views.shipment_detail, name='shipment_detail'),
path('profile/', views.profile, name='profile'),
path('my-shipments/', views.my_shipments, name='my_shipments'),
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Collectstatic

```bash
python manage.py collectstatic --no-input
```

---

## Database Migration (SQLite to PostgreSQL)

### Step 1: Install PostgreSQL Driver
```bash
pip install psycopg2-binary
```

### Step 2: Update `settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fleeting_logistics',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 3: Dump Data (if needed)
```bash
python manage.py dumpdata > data.json
```

### Step 4: Create New Database
```bash
createdb fleeting_logistics
```

### Step 5: Run Migrations
```bash
python manage.py migrate
python manage.py loaddata data.json  # if needed
```

---

## Performance Optimization Checklist

- [ ] Enable GZIP compression in Nginx
- [ ] Implement browser caching headers
- [ ] Compress images (use TinyPNG/ImageOptim)
- [ ] Minify CSS and JavaScript
- [ ] Set up CDN for static files
- [ ] Use database indexes on frequently queried fields
- [ ] Implement Redis caching
- [ ] Use async tasks for heavy operations
- [ ] Optimize database queries (select_related, prefetch_related)
- [ ] Test with Google PageSpeed Insights

---

## Security Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS everywhere
- [ ] Set CSRF cookie secure
- [ ] Set SESSION cookie secure
- [ ] Add security headers (CSP, X-Frame-Options)
- [ ] Implement rate limiting
- [ ] Validate and sanitize all inputs
- [ ] Use parameterized queries (Django ORM)
- [ ] Update dependencies regularly

### Add Security Headers (`settings.py`)
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

---

## Deployment Options

### Option 1: Heroku (Easiest)
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
```

### Option 2: DigitalOcean (Affordable)
- Create Droplet
- Install Python, Postgres, Nginx
- Clone repository
- Install requirements
- Configure Nginx
- Set up SSL with Let's Encrypt
- Use systemd for process management

### Option 3: AWS EC2
- Launch EC2 instance (Ubuntu)
- Install dependencies
- Configure security groups
- Set up RDS for database
- Use Elastic IP
- Set up Route 53 for DNS

---

## Monitoring & Analytics

### Error Tracking (Sentry)
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### Performance Monitoring
- Set up New Relic or DataDog
- Monitor database query times
- Track API response times
- Set up Uptime monitoring

---

## Future Enhancements

1. **Real-time Tracking**: Integrate GPS/mapping API
2. **Payment Gateway**: Add Stripe/PayPal integration
3. **Mobile App**: Build React Native app
4. **AI Chatbot**: Add customer support bot
5. **Analytics Dashboard**: Create detailed analytics
6. **Admin Portal**: Advanced admin features
7. **Email Notifications**: Automated email updates
8. **SMS Notifications**: SMS tracking updates
9. **Rating System**: Customer reviews
10. **Referral Program**: Rewards system

---

## Contact & Support

For questions or support, contact:
- Email: dev@fleetinglogistics.com
- Phone: +256 752 276 350
- WhatsApp: [Link](https://wa.me/256752276350)

---

**Last Updated**: May 9, 2026
**Version**: 1.0
