from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def showcase(request):
    return render(request, 'showcase.html')

def testimonials(request):
    return render(request, 'testimonals.html')

def contact(request):
    return render(request, 'contactus.html')

def booking(request):
    return render(request, 'bookingForm.html')

def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')
            
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        login(request, user)
        return redirect('home')
        
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')