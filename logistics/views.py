from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        # Handle form submission (for now, just pass)
        pass
    return render(request, 'contact.html')

def booking(request):
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        pickup_location = request.POST.get('pickup_location')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        message = request.POST.get('message')
        
        booking = Booking.objects.create(
            service_type=service_type,
            name=name,
            phone=phone,
            email=email,
            pickup_location=pickup_location,
            destination=destination,
            date=date,
            message=message
        )
        messages.success(request, 'Your booking request has been submitted successfully!')
        return redirect('booking')
    return render(request, 'booking.html')
