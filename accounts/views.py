from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST)  # Remove 'or None', it's not needed for POST
            
            if form.is_valid():
                # Save the user - this returns the user object already
                user = form.save()
                
                # No need to authenticate here! The user is already created and valid
                # Just log them in directly
                login(request, user)
                
                return redirect("main:home")
        else:
            form = RegistrationForm()
        
        return render(request, "accounts/register.html", {"form": form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")

                else:
                    return render(request, 'accounts/login.html', {"error": "Your account has been disabled"})
            else:
                return render(request, 'accounts/login.html', {"error": "Invalid username or password"})
        return render(request, 'accounts/login.html')

def logout_user(request):
    if request.user.is_authenticated:
    
        logout(request)
        print("Logged out")
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")