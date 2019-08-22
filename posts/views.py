from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Category, Post, Attachment
from django.db.models import Count
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse


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
            if 'attach_file' in request.FILES:
                is_attached = True
            else:
                is_attached = False
            # validation
            title = request.POST['post_title']
            desc = request.POST['post_description']
            body = request.POST['post_body']
            cat = request.POST['post_category_id']
            author = request.user
            is_valid = True

            if not(20 <= len(title) <= 200):
                messages.error(
                    request, 'Title length must be between 20 and 200 caracters')
                is_valid = False
            if not(100 <= len(desc) <= 390):
                messages.error(
                    request, 'Description must be between 100 and 380 caracters')
                is_valid = False
            if not(len(body) > 400):
                messages.error(request,
                               'Post Content must be larger than 400 caracters')
                is_valid = False

            if not(cat.isdigit()):
                messages.error(
                    request, 'You must choose a valid category for your post')
                is_valid = False
            else:
                category = get_object_or_404(
                    Category, pk=cat)
                if not category:
                    messages.error(
                        request, 'There is no such category with id  : '+cat)
                    is_valid = False

            if is_attached:
                attachment = request.FILES['attach_file']
            if attachment.size > 5000000:
                messages.error(request, 'Max file size is 5 Mb')
                is_valid = False

            if is_valid:
                post = Post(title=title, body=body,  author=author,
                            category=category)
                post.save()
                messages.success(request, 'Posted!!!!!!!!')
                if is_attached:
                    att = Attachment(post=post, attachment=attachment)
                    att.save()
                    print('file primary key')
                    print(att.pk)
                return redirect('single_post', post_id=post.pk, post_slug=post.slug)

            context = {
                'categories': categories,
                'values': request.POST
            }
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


def single_post(request, post_id, post_slug):
    post = get_object_or_404(Post, pk=post_id)
    attachments = Attachment.objects.filter(post__id=post_id)
    context = {
        'post': post,
        'attachments': attachments
    }
    print(context)

    return render(request, 'posts/single_post.html', context)
