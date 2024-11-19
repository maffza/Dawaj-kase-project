from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
import hashlib

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

        with connection.cursor() as cursor:
            cursor.execute("SELECT email, password_hash, first_name FROM users WHERE email=%s", [email])
            row = cursor.fetchone()

        if row:
            userEmail, userPasswordHash, userFirstName = row[0], row[1], row[2]

            hashedPassword = hashlib.sha256(password.encode()).hexdigest()

            if hashedPassword == userPasswordHash:
                request.session['user_email'] = userEmail
                request.session['user_first_name'] = userFirstName
                return redirect('index')
            else:
                messages.error(request, "Invalid password.")
        else:
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