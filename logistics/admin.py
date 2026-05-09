from django.contrib import admin
from .models import (
    Booking, Service, UserProfile, Shipment, 
    TrackingUpdate, Notification, ContactMessage
)


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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'role', 'verified', 'email_verified', 'created_at')
    list_filter = ('role', 'verified', 'email_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone', 'role')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Verification', {
            'fields': ('verified', 'email_verified', 'phone_verified')
        }),
        ('Profile', {
            'fields': ('profile_picture',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class TrackingUpdateInline(admin.TabularInline):
    model = TrackingUpdate
    extra = 1
    readonly_fields = ('timestamp',)
    fields = ('status', 'location', 'message', 'updated_by', 'timestamp')


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'customer', 'receiver_name', 'status', 'vehicle_type', 'total_price', 'is_paid', 'pickup_date')
    list_filter = ('status', 'vehicle_type', 'is_paid', 'pickup_date', 'created_at')
    search_fields = ('tracking_id', 'customer__username', 'receiver_name', 'receiver_phone')
    readonly_fields = ('tracking_id', 'created_at', 'updated_at')
    inlines = [TrackingUpdateInline]
    
    fieldsets = (
        ('Tracking', {
            'fields': ('tracking_id', 'status', 'current_location')
        }),
        ('Customer Information', {
            'fields': ('customer',)
        }),
        ('Sender Information', {
            'fields': ('sender_name', 'sender_phone', 'sender_email')
        }),
        ('Receiver Information', {
            'fields': ('receiver_name', 'receiver_phone', 'receiver_email')
        }),
        ('Pickup & Delivery', {
            'fields': ('pickup_location', 'destination', 'pickup_date', 'estimated_delivery', 'actual_delivery')
        }),
        ('Shipment Details', {
            'fields': ('description', 'weight', 'vehicle_type')
        }),
        ('Pricing', {
            'fields': ('distance_km', 'base_price', 'surcharge', 'total_price')
        }),
        ('Payment', {
            'fields': ('is_paid', 'payment_method')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new shipment
            obj.save()
        else:
            obj.save()


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'is_sent', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_sent', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')
    actions = ['mark_as_sent', 'mark_as_read']
    
    def mark_as_sent(self, request, queryset):
        updated = queryset.update(is_sent=True)
        self.message_user(request, f'{updated} notifications marked as sent.')
    mark_as_sent.short_description = 'Mark selected as sent'
    
    def mark_as_read(self, request, queryset):
        for notification in queryset:
            notification.mark_as_read()
        self.message_user(request, f'{queryset.count()} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected as read'


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_replied', 'created_at')
    list_filter = ('is_replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'replied_at')
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Reply', {
            'fields': ('is_replied', 'reply_message', 'replied_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# Register your models here
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(TrackingUpdate)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
