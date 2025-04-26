from django.contrib import admin
from .models import BookingForm

@admin.register(BookingForm)
class BookingFormAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'event_type', 'full_name', 'event_date', 'status')
    list_filter = ('event_type', 'status', 'event_date')
    search_fields = ('booking_reference', 'first_name', 'last_name', 'email')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'start_time', 'end_time', 'estimated_guests', 'budget_range')
        }),
        ('Customization', {
            'fields': ('venue_type', 'theme', 'special_requirements')
        }),
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'additional_notes')
        }),
        ('System Information', {
            'fields': ('status', 'assigned_manager', 'booking_reference', 'created_at', 'updated_at')
        }),
    )