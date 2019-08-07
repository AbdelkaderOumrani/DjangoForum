from django.shortcuts import render, redirect
from .models import Category, Post
from django.db.models import Count
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required


def categories(request):
    categories = Category.objects.annotate(nb_posts=Count('post'))
    context = {
        'categories': categories
    }
    return render(request, 'pages/categories.html', context)


@login_required(redirect_field_name='login')
def recent_posts(request):
    posts = Post.objects.all().order_by('-created')
    context = {
        'posts': posts
    }
    return render(request, 'posts/recent_posts.html', context)


@login_required(redirect_field_name='new_post')
def new_post(request):
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
