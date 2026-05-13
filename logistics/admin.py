from django.contrib import admin
from .models import Booking, Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'service', 'phone', 'pickup_location', 'destination', 'date', 'status')
    list_filter = ('service', 'status', 'date')
    search_fields = ('name', 'phone', 'email')
    list_editable = ('status',)
    ordering = ('-created_at',)

# Register your models here.
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)
