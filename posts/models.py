from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Category Class


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    COLOR_CHOICES = (
        ('primary', 'Blue'),
        ('success', 'Green'),
        ('info', 'Sky Blue'),
        ('warning', 'Yellow'),
        ('danger', 'Red')
    )

    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visited = models.IntegerField(default=0)
    color = models.CharField(
        max_length=20, default='primary', choices=COLOR_CHOICES)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    STATUS_CHOICES = (
        (True, 'Visible'),
        (False, 'Hidden')
    )
    title = models.CharField(max_length=250)
    body = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS_CHOICES = (
        (True, 'Visible'),
        (False, 'Hidden')
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)
