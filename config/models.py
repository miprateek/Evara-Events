from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone



class ContactUs(models.Model):
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    # Event Details
    event_type = models.CharField(
        max_length=20,
        choices=[
            ('wedding', 'Wedding'),
            ('corporate', 'Corporate Event'),
            ('birthday', 'Birthday Party'),
            ('festival', 'Festival'),
            ('other', 'Other'),
        ]
    )
    event_date = models.DateField(null=True, blank=True)
    
    # Budget Information
    budget_range = models.CharField(
        max_length=10,
        choices=[
            ('5k-10k', '₹5,000 - ₹10,000'),
            ('10k-25k', '₹10,000 - ₹25,000'),
            ('25k-50k', '₹25,000 - ₹50,000'),
            ('50k+', '₹50,000+'),
        ]
    )
    
    # Message
    message = models.TextField()
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,  # Increased from 10 to 15
        choices=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='new'
    )
    
    class Meta:
        verbose_name = 'Contact Form Submission'
        verbose_name_plural = 'Contact Form Submissions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event_type} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def mark_in_progress(self):
        self.status = 'in_progress'
        self.save()
    
    def mark_completed(self):
        self.status = 'completed'
        self.save()

class MapSettings(models.Model):
    location_name = models.CharField(max_length=100)
    map_url = models.TextField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Map Setting"
        verbose_name_plural = "Map Settings"

    def __str__(self):
        return self.location_name

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other locations as non-default
            MapSettings.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

