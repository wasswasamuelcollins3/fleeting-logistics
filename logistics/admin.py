from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_type', 'pickup_location', 'destination', 'date')
    list_filter = ('service_type', 'date')
    search_fields = ('name', 'phone')
    ordering = ('-created_at',)

# Register your models here.
admin.site.register(Booking, BookingAdmin)
