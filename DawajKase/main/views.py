from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
import hashlib
from .ManagerFactory import ManagerFactory

# Create your views here.
def index(request):
    return render(request, 'DawajKase/index.html')

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
            request.session['user_first_name'] = ret[1].name
            request.session['user_email'] = ret[1].email
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
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM users WHERE email=%s", [email])
            row = cursor.fetchone()

        if row:
            messages.error(request, "The email address is already in use.")
            return redirect('/auth?register=1')  

        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users(first_name, last_name, address, city, email, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           [firstName, lastName, address, city, email, hashedPassword, "Supporter"])

    else:
        pass

    return redirect('auth')

def logout(request):
    request.session.flush()
    return redirect('index')

def project(request):
    return render(request, 'DawajKase/project.html')