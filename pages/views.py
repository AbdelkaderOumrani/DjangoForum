from django.shortcuts import render, redirect
from posts.models import Category
from django.db.models import Count
from django.contrib.auth.models import User


def index(request):
    return redirect('recent_posts')


def categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.annotate(nb_posts=Count('post'))
        context = {
            'categories': categories
        }
        return render(request, 'pages/categories.html', context)
    else:
        return redirect('login')
