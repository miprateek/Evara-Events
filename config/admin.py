from django.contrib import admin
from .models import MapSettings, ContactUs

@admin.register(MapSettings)
class MapSettingsAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'is_default', 'created_at', 'updated_at')
    list_filter = ('is_default',)
    search_fields = ('location_name',)
    ordering = ('-is_default', 'location_name')



@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event_type', 'created_at', 'status')
    list_filter = ('event_type', 'status')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)