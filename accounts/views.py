from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('categories')
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if (password == password2):
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                    username=username, email=email, password=password)
                    auth.login(request, user)
                    return redirect('categories')

        else:
            messages.error(request, 'Password do not match')
            return redirect('register')

    return render(request, 'accounts/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('categories')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('categories')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    username = request.user.username
    django_logout(request)
    messages.success(request, username + 'You are now logged out')
    return HttpResponseRedirect('login')


def edit_profil(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/edit_profile.html')


def show_profil(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/show_profile.html')
