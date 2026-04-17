from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking
import urllib.parse

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
        
        # Save booking to database
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
        
        # Format WhatsApp message
        whatsapp_message = f"""Hello Fleeting Logistics,
I would like to book a service.

Service Type: {service_type}
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
    
    return render(request, 'booking.html')
