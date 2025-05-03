from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EventBookingForm
from .models import BookingForm

@login_required
def booking_view(request):
    if request.method == 'POST':
        form = EventBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()
            messages.success(request, f'Booking submitted successfully! Your reference number is {booking.booking_reference}')
            return redirect('booking:booking')
    else:
        form = EventBookingForm()
    
    return render(request, 'bookingForm.html', {'form': form})

@login_required
def booking_list_view(request):
    bookings = BookingForm.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {
        'bookings': bookings
    })

@login_required
def display_bookings(request):
    if request.user.is_authenticated:
        # Get all bookings for the logged-in user
        user_bookings = BookingForm.objects.filter(user=request.user).order_by('-created_at')
        context = {
            'bookings': user_bookings
        }
        return render(request, 'bookings.html', context)
    return redirect('login')