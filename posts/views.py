from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Category, Post, Attachment, Comment
from django.contrib.auth.models import User
from django.db.models import Count, Q, Max, F
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse


def categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.order_by('rank','-created').annotate(nb_posts=Count('post'))
        
        posts = list()
        for category in categories:
            if Post.objects.filter(category=category).filter(status=True).count():
                posts.append(category.post_set.latest('created'))
        context = {
            'posts':posts,
            'categories': categories
            }
        return render(request, 'posts/categories.html', context)
    else:
        return redirect('login')


def recent_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().filter(status=True).order_by(
            '-created').annotate(nb_comments = Count('comment'))
        
        comments = list()
        for post in posts:
            if Comment.objects.filter(post=post).count():
                comments.append(post.comment_set.latest('created'))
        context={
            'posts': posts,
            'comments':comments
        }
        return render(request, 'posts/recent_posts.html', context)
    else:
        messages.error(request, 'You must log in first')
        return redirect('login')



def posts_by_category(request, category_id, category_slug):
    posts = Post.objects.all().filter(category__slug=category_slug)
    category = Category.objects.get(pk=category_id)
    category.visited += 1
    category.save()

    context = {
        'category': category,
        'posts': posts
    }

    return render(request, 'posts/posts_by_category.html', context)


def single_post(request, post_id, post_slug):
    post = get_object_or_404(Post, pk=post_id)
    post.visited += 1
    post.save()
    author_nb_posts = Post.objects.filter(author=post.author).count()
    attachments = Attachment.objects.filter(post__id=post_id)
    post_comments = Comment.objects.filter(post=post).filter(status=True)
    context = {
        'author_nb_posts': author_nb_posts,
        'post': post,
        'attachments': attachments,
        'post_comments': post_comments
    }
    return render(request, 'posts/single_post.html', context)


def add_new_comment(request, post_id):
    if request.POST:
        post = get_object_or_404(Post, pk=post_id)
        comment = request.POST['inputNewComment']
        c = Comment(post=post, body=comment,  author=request.user)
        c.save()
    return redirect('single_post', post_id=post.id, post_slug=post.slug)

def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect(single_post, post_id=comment.post.id , post_slug=comment.post.slug)

def delete_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request,'Your Post deleted successfully')
        return redirect('recent_posts')
    else:
        messages.error(request,'You have no authorization')
        return redirect('recent_posts')



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
            body = request.POST['post_body']
            cat = request.POST['post_category_id']
            author = request.user
            is_valid = True

            if not(len(title) <= 200):
                messages.error(
                    request, 'Title length must be between 20 and 200 caracters')
                is_valid = False
            if not(len(body) > 10):
                messages.error(request,
                               'Post Content must be larger than 10 caracters')
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
                if is_attached:
                    att = Attachment(post=post, attachment=attachment)
                    att.save()
                return redirect('single_post', post_id=post.pk, post_slug=post.slug)

            context = {
                'categories': categories,
                'values': request.POST
            }
        return render(request, 'posts/new_post.html', context)
    else:
        return redirect('login')




def edit_post(request,post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=post_id)
        context = {
            'post':post,
                'categories': categories
            }
        if request.POST:
            if 'attach_file' in request.FILES:
                is_attached = True
            else:
                is_attached = False
            # validation
            title = request.POST['post_title']
            body = request.POST['post_body']
            cat = request.POST['post_category_id']
            is_valid = True

            if not(len(title) <= 200):
                messages.error(
                    request, 'Title length must be between 20 and 200 caracters')
                is_valid = False
            if not(len(body) > 10):
                messages.error(request,
                               'Post Content must be larger than 10 caracters')
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
                post.title=title
                post.body=body
                post.category=category
                post.save()
                if is_attached:
                    att = Attachment(post=post, attachment=attachment)
                    att.save()
                return redirect('single_post', post_id=post.pk, post_slug=post.slug)

            context = {
                'categories': categories,
                'values': request.POST,
                'post':post
            }
        return render(request, 'posts/edit_post.html', context)
    else:
        return redirect('login')


def search_posts(request,search_val):
    if request.user.is_authenticated:
        if request.POST:
            if request.POST['search_val']:
                search_val = request.POST['search_val']
            else:
                search_val = request.POST['search_val2']
            return redirect('search_posts',search_val=search_val)

    else:
        return redirect('login')
    posts = Post.objects.filter(Q(title__icontains=search_val)|
                                Q(body__icontains=search_val)).filter(status=True)
    context = {
        'search_val':search_val,
        'posts':posts
    }
    return render(request, 'posts/search.html',context)

def my_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user)
        context = {
            'posts':posts
        }
        return render(request,'posts/my_posts.html',context)
    else:
        return redirect(login)
