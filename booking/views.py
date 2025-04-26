from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EventBookingForm

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