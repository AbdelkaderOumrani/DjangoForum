from django.shortcuts import render, redirect


def landing_page(request):
    auth = False
    if request.user.is_authenticated:
        auth = True

    return render(request, 'pages/landing_page.html', {'auth': auth})
