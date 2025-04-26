from django import forms
from .models import BookingForm
from django.utils import timezone

class EventBookingForm(forms.ModelForm):
    class Meta:
        model = BookingForm
        exclude = ['status', 'created_at', 'updated_at', 'booking_reference', 'assigned_manager']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'special_requirements': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any specific requirements or preferences?'}),
            'additional_notes': forms.Textarea(attrs={'rows': 4, 'placeholder': "Any additional information you'd like to share?"})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        event_date = cleaned_data.get('event_date')

        if event_date and event_date < timezone.now().date():
            raise forms.ValidationError("Event date cannot be in the past")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time")