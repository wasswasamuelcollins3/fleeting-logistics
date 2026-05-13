from django.contrib import admin

from .models import Booking, ContactMessage, Service, Shipment


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "service",
        "phone",
        "pickup_location",
        "destination",
        "date",
        "status",
    )
    list_filter = ("service", "status", "date")
    search_fields = ("name", "phone", "email")
    list_editable = ("status",)
    ordering = ("-created_at",)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-created_at",)


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("tracking_id", "user", "service", "status", "created_at")
    list_filter = ("status", "service")
    search_fields = ("tracking_id", "sender_email", "recipient_email", "sender_name")
    ordering = ("-created_at",)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Shipment, ShipmentAdmin)
