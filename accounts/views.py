from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


def register(request):
    return render(request, 'accounts/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')
    print(request)


def logout(request):
    username = request.user.username
    django_logout(request)
    messages.success(request, username + 'You are now logged out')
    return HttpResponseRedirect('login')
