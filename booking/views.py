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
            booking.user = request.user  # Associate the booking with the current user
            booking.save()
            messages.success(request, f'Booking submitted successfully! Your reference number is {booking.booking_reference}')
            return redirect('booking:booking')
    else:
        form = EventBookingForm()
    
    return render(request, 'bookingForm.html', {'form': form})

@login_required
def booking_list_view(request):
    bookings = BookingForm.objects.all().order_by('-created_at')
    return render(request, 'booking_list.html', {
        'bookings': bookings
    })

@login_required
def display_bookings(request):
    # No need to check if user is authenticated since @login_required already handles this
    
    # Get all bookings for the logged-in user
    # Assuming you have a user field in your BookingForm model
    user_bookings = BookingForm.objects.filter(user=request.user).order_by('-created_at')
    
    # Add a message if no bookings are found
    if not user_bookings.exists():
        messages.info(request, "You don't have any bookings yet.")
    
    context = {
        'bookings': user_bookings,
        'page_title': 'My Bookings'
    }
    
    return render(request, 'bookings.html', context)