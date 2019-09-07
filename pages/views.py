from django.shortcuts import render, redirect
from posts.models import Category
from django.db.models import Count
from django.contrib.auth.models import User


def index(request):
    return redirect('recent_posts')
