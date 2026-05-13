import logging
import urllib.parse
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Booking, ContactMessage, Service, Shipment

logger = logging.getLogger(__name__)


def _decimal_or_none(value):
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def contact(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        message = (request.POST.get("message") or "").strip()
        subject = (request.POST.get("subject") or "").strip() or "Website contact form"

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        body = f"From: {name} ({email})\nPhone: {phone or '—'}\n\nMessage:\n{message}"
        try:
            send_mail(
                f"Contact Form: {subject}",
                body,
                settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception:
            logger.exception("Contact form: failed to send admin email")
            messages.error(
                request,
                "Sorry, there was an error sending your message. Please try again or call us directly.",
            )

        return redirect("contact")

    return render(request, "contact.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    return render(request, "profile.html")


def tracking(request):
    query = request.GET.get("query", "").strip()
    booking_results = []
    shipment_results = []
    if query:
        q_booking = (
            Q(name__icontains=query)
            | Q(phone__icontains=query)
            | Q(email__icontains=query)
        )
        if query.isdigit():
            q_booking |= Q(pk=query)
        booking_results = list(
            Booking.objects.filter(q_booking).select_related("service").order_by("-created_at")
        )

        q_shipment = (
            Q(tracking_id__iexact=query)
            | Q(tracking_id__icontains=query)
            | Q(sender_email__icontains=query)
            | Q(sender_phone__icontains=query)
            | Q(recipient_email__icontains=query)
            | Q(recipient_phone__icontains=query)
            | Q(sender_name__icontains=query)
            | Q(recipient_name__icontains=query)
        )
        shipment_results = list(
            Shipment.objects.filter(q_shipment).select_related("service").order_by("-created_at")
        )

        if not booking_results and not shipment_results:
            messages.warning(
                request,
                "No bookings or shipments were found for that search term.",
            )

    return render(
        request,
        "tracking.html",
        {
            "booking_results": booking_results,
            "shipment_results": shipment_results,
            "query": query,
        },
    )


def booking(request):
    quote_mode = request.GET.get("quote") == "true"
    services_qs = Service.objects.filter(is_active=True)

    if request.method == "POST":
        service_id = request.POST.get("service")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        pickup_location = request.POST.get("pickup_location")
        destination = request.POST.get("destination")
        date = request.POST.get("date")
        time = request.POST.get("time")
        message = request.POST.get("message")
        estimated_distance = request.POST.get("estimated_distance")
        vehicle_rate = request.POST.get("vehicle_rate")
        estimated_cost = request.POST.get("estimated_cost")

        try:
            service = Service.objects.get(id=service_id)
        except (Service.DoesNotExist, TypeError, ValueError):
            messages.error(request, "Invalid service selected.")
            return redirect("booking")

        Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            service=service,
            name=name,
            phone=phone,
            email=email,
            pickup_location=pickup_location,
            destination=destination,
            date=date,
            time=time,
            estimated_distance=float(estimated_distance) if estimated_distance else None,
            vehicle_rate=_decimal_or_none(vehicle_rate),
            estimated_cost=_decimal_or_none(estimated_cost),
            message=message,
        )

        subject = f"Booking Confirmation - {service.name}"
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
        from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
        try:
            send_mail(
                subject,
                customer_message,
                from_email,
                [email],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Booking: customer confirmation email failed")
            messages.warning(
                request,
                "Booking saved but email confirmation could not be sent.",
            )

        admin_subject = f"New Booking Request - {service.name}"
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
                from_email,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Booking: admin notification email failed")

        whatsapp_message = f"""Hello Fleeting Logistics,
I would like to book a service.

Service: {service.name}
Name: {name}
Phone: {phone}
Pickup: {pickup_location}
Destination: {destination}
Date: {date}
Details: {message}"""

        encoded_message = urllib.parse.quote(whatsapp_message)
        wa_digits = getattr(settings, "WHATSAPP_PHONE_DIGITS", "256768383164")
        whatsapp_url = f"https://wa.me/{wa_digits}?text={encoded_message}"

        messages.success(
            request,
            "Your booking request has been submitted successfully! Redirecting to WhatsApp...",
        )

        return redirect(whatsapp_url)

    return render(
        request,
        "booking.html",
        {
            "services": services_qs,
            "quote_mode": quote_mode,
        },
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
