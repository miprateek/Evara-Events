from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class BookingForm(models.Model):
    # Event Types
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate Event'),
        ('birthday', 'Birthday Party'),
        ('festival', 'Festival'),
        ('product-launch', 'Product Launch'),
        ('other', 'Other'),
    ]

    # Budget Ranges
    BUDGET_RANGES = [
        ('5k-10k', '$5,000 - $10,000'),
        ('10k-25k', '$10,000 - $25,000'),
        ('25k-50k', '$25,000 - $50,000'),
        ('50k-100k', '$50,000 - $100,000'),
        ('100k+', '$100,000+'),
    ]

    # Venue Types
    VENUE_TYPES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('both', 'Both'),
    ]

    # Theme Options
    THEME_OPTIONS = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('rustic', 'Rustic'),
        ('luxury', 'Luxury'),
        ('custom', 'Custom'),
    ]

    # Status Choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    # Event Details
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    estimated_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    budget_range = models.CharField(max_length=10, choices=BUDGET_RANGES)

    # Customization Options
    venue_type = models.CharField(max_length=10, choices=VENUE_TYPES)
    theme = models.CharField(max_length=10, choices=THEME_OPTIONS)
    special_requirements = models.TextField(blank=True)

    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    additional_notes = models.TextField(blank=True)

    # System Fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking_reference = models.CharField(max_length=10, unique=True, blank=True)
    assigned_manager = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_bookings'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.first_name} {self.last_name} - {self.event_date}"

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate a unique booking reference
            prefix = self.event_type[:3].upper()
            timestamp = timezone.now().strftime('%y%m%d')
            random_digits = str(self.id)[-4:].zfill(4) if self.id else '0000'
            self.booking_reference = f"{prefix}-{timestamp}-{random_digits}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def event_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def is_upcoming(self):
        return self.event_date > timezone.now().date()

    @property
    def is_past(self):
        return self.event_date < timezone.now().date()

    @property
    def is_today(self):
        return self.event_date == timezone.now().date()

    def get_budget_range_display(self):
        return dict(self.BUDGET_RANGES).get(self.budget_range, '')

    def get_venue_type_display(self):
        return dict(self.VENUE_TYPES).get(self.venue_type, '')

    def get_theme_display(self):
        return dict(self.THEME_OPTIONS).get(self.theme, '')

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')

    def confirm_booking(self):
        self.status = 'confirmed'
        self.save()

    def cancel_booking(self):
        self.status = 'cancelled'
        self.save()

    def complete_booking(self):
        self.status = 'completed'
        self.save() 