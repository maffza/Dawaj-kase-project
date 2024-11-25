from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
import hashlib
from .ManagerFactory import ManagerFactory

# Create your views here.
def index(request):
    userData = request.session.get('userData', None)

    return render(request, 'DawajKase/index.html', {'userData': userData})

def auth(request):
    register = request.GET.get('register', None)
    return render(request, 'DawajKase/auth.html', {'register': register})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        UserManager = ManagerFactory.get_user_manager()

        ret = UserManager.log_user_in(email, password)
        
        if ret[0] == "OK":
            user = ret[1]
            request.session['userData'] = user.to_json()
            return redirect('index')
        elif ret[0] == "InvalidPassword":
            messages.error(request, "Invalid password.")
        elif ret[0] == "InvalidEmail":
            messages.error(request, "Invalid email.")
        
    else:
        pass                  

    return redirect('auth')

def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstname')
        lastName = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if password != confirmPassword:
            messages.error(request, "Passwords are not the same.")
            return redirect('/auth?register=1')

        UserManager = ManagerFactory.get_user_manager()

        if UserManager.check_if_user_exists(email):
            messages.error(request, "The email address is already in use.")
            return redirect('/auth?register=1')

        UserManager.register_user(firstName, lastName, email, password, city, address)

    else:
        pass

    return redirect('auth')

def logout(request):
    request.session.flush()
    return redirect('index')

def project(request):
    return render(request, 'DawajKase/project.html')