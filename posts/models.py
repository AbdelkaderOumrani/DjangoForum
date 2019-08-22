from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

    title = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200,)
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
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=400, default='desc')
    body = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='img/posts', blank=True)
    slug = models.SlugField(max_length=200,)
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Post)
def photo_post_delete_handler(sender, **kwargs):
    listingImage = kwargs['instance']
    storage, path = listingImage.image.storage, listingImage.image.path
    storage.delete(path)


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    attachment = models.FileField(upload_to='attachments', blank=False)


@receiver(post_delete, sender=Attachment)
def submission_delete(sender, instance, **kwargs):
    instance.attachment.delete(False)


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


# class Bookmark(models.Model):
