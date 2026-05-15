from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Booking, Service
import urllib.parse

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email to admin
        try:
            send_mail(
                f'Contact Form Message from {name}',
                f'From: {name} ({email})\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')

        return redirect('contact')

    return render(request, 'contact.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')

    return render(request, 'profile.html')

def tracking(request):
    query = request.GET.get('query', '').strip()
    results = []
    if query:
        q = Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query)
        if query.isdigit():
            q |= Q(pk=query)
        results = Booking.objects.filter(q).order_by('-created_at')
        if not results:
            messages.warning(request, 'No bookings or shipments were found for that search term.')

    return render(request, 'tracking.html', {
        'results': results,
        'query': query,
    })

def booking(request):
    try:
        services = Service.objects.filter(is_active=True)
        
        if request.method == 'POST':
        try:
            service_id = request.POST.get('service')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            pickup_location = request.POST.get('pickup_location')
            destination = request.POST.get('destination')
            date = request.POST.get('date')
            time = request.POST.get('time')
            message = request.POST.get('message')
            estimated_distance = request.POST.get('estimated_distance')
            vehicle_rate = request.POST.get('vehicle_rate')
            estimated_cost = request.POST.get('estimated_cost')
            
            try:
                service = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                messages.error(request, 'Invalid service selected.')
                return redirect('booking')
        
        # Save booking to database
        try:
            est_distance = float(estimated_distance) if estimated_distance and estimated_distance.strip() else None
        except (ValueError, AttributeError):
            est_distance = None
            
        try:
            v_rate = float(vehicle_rate) if vehicle_rate and vehicle_rate.strip() else None
        except (ValueError, AttributeError):
            v_rate = None
            
        try:
            est_cost = float(estimated_cost) if estimated_cost and estimated_cost.strip() else None
        except (ValueError, AttributeError):
            est_cost = None
        
        booking = Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            service=service,
            name=name,
            phone=phone,
            email=email,
            pickup_location=pickup_location,
            destination=destination,
            date=date,
            time=time,
            estimated_distance=est_distance,
            vehicle_rate=v_rate,
            estimated_cost=est_cost,
            message=message
        )
        
        # Send confirmation email to customer
        subject = f'Booking Confirmation - {service.name}'
        customer_message = f"""
Dear {name},

Thank you for booking with Fleeting Logistics Company Limited!

Booking Details:
- Service: {service.name}
- Pickup Location: {pickup_location}
- Destination: {destination}
- Date: {date}
- Phone: {phone}

Your booking request has been received and our team will contact you shortly.

Best regards,
Fleeting Logistics Team
"""
        try:
            send_mail(
                subject,
                customer_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            messages.warning(request, 'Booking saved but email confirmation could not be sent.')
        
        # Send notification email to admin
        admin_subject = f'New Booking Request - {service.name}'
        admin_message = f"""
New booking received:

Customer: {name}
Email: {email}
Phone: {phone}
Service: {service.name}
From: {pickup_location}
To: {destination}
Date: {date}
Message: {message or 'None'}

Please contact the customer to confirm the booking.
"""
        try:
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],  # Send to admin email
                fail_silently=False,
            )
        except Exception as e:
            pass  # Admin notification failure shouldn't affect user experience
        
        # Format WhatsApp message
        whatsapp_message = f"""Hello Fleeting Logistics,
I would like to book a service.

Service: {service.name}
Name: {name}
Phone: {phone}
Pickup: {pickup_location}
Destination: {destination}
Date: {date}
Details: {message}"""
        
        # URL encode the message
        encoded_message = urllib.parse.quote(whatsapp_message)
        
        # WhatsApp URL
        whatsapp_url = f"https://wa.me/256768383164?text={encoded_message}"
        
        messages.success(request, 'Your booking request has been submitted successfully! Redirecting to WhatsApp...')
        
        # Redirect to WhatsApp
        return redirect(whatsapp_url)
        
        except Exception as e:
            # Log the error and show a user-friendly message
            import traceback
            print(f"Booking error: {str(e)}")
            print(traceback.format_exc())
            messages.error(request, f'An error occurred while processing your booking: {str(e)}')
            return redirect('booking')
        
        services = Service.objects.filter(is_active=True)
        return render(request, 'booking.html', {'services': services})
    
    except Exception as e:
        import traceback
        print(f"Booking view error: {str(e)}")
        print(traceback.format_exc())
        # Return a simple error page or redirect to home
        messages.error(request, 'An error occurred while loading the booking page. Please try again.')
        return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
