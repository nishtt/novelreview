from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST) 
            
            if form.is_valid():
                user = form.save()
                login(request, user)
                
                return redirect("main:home")
        else:
            form = RegistrationForm()
        
        return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')  

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                
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