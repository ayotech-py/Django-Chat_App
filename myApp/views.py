import email
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Services
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    services = Services.objects.all()
    return render(request, 'index.html', {'services': list(services)})


def counter(request):
    text = request.POST['text']
    word_count = len(text.split())
    return render(request, 'counter.html', {'amount': word_count})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already Used")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already Used")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                messages.info(request, "Account succesfully created")
                return redirect('/chatapp/login')
        else:
            messages.info(request, "password mismatch")
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request, pk):
    return render(request, 'profile.html', {'username': pk})
