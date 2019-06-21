from django.shortcuts import render, redirect
from .models import Category, Post
from django.db.models import Count


def categories(request):
    categories = Category.objects.annotate(nb_posts=Count('post'))
    context = {
        'categories': categories
    }
    return render(request, 'pages/categories.html', context)


def new_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        if request.method == 'POST':
            title = request.POST['title']
            body = request.POST['post_body']
            #category = request.POST['post_category']
            author = request.user
            post = Post(title=title, body=body,  author=author)
            post.save()
            return redirect('categories')
        return render(request, 'posts/new_post.html', context)
