from django.shortcuts import render, redirect
from posts.models import Category
from django.db.models import Count


def index(request):
    return redirect('categories')


def categories(request):
    categories = Category.objects.annotate(nb_posts=Count('post'))
    context = {
        'categories': categories
    }
    return render(request, 'pages/categories.html', context)
