from django.shortcuts import render, redirect, get_list_or_404
from .models import Category, Post
from django.db.models import Count
from django.contrib import messages


def categories(request):
    categories = Category.objects.annotate(nb_posts=Count('post'))
    context = {
        'categories': categories
    }
    return render(request, 'pages/categories.html', context)


def recent_posts(request):
    posts = Post.objects.all().order_by('-created')
    context = {
        'posts': posts
    }
    return render(request, 'posts/recent_posts.html', context)


def new_post(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        if request.POST:
            messages.error(request, 'Post Request')
            title = request.POST['post_title']
            body = request.POST['post_body']
            cover = request.POST['post_cover']
            #category = request.POST['post_category']
            author = request.user
            post = Post(title=title, body=body,  author=author,cover=cover)
            post.save()
            return redirect('new_post')
        return render(request, 'posts/new_post.html', context)
    else:
        return redirect('login')


def posts_by_category(request, category_slug):
    posts = get_list_or_404(Post, category__slug=category_slug)
    category = posts[0].category.title

    context = {
        'category': category,
        'posts': posts
    }

    return render(request, 'posts/posts_by_category.html', context)
