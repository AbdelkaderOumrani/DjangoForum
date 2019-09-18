from django.contrib import admin
from .models import Category, Post, Comment, Attachment


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'description', 'created',
                    'updated', 'slug', 'rank')
    sortable_by = ('rank')


class PostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'author', 'category', 'status',
                    'created', 'updated')
    list_filter = ('status', 'category')
    search_fields = ('title', 'body')
    sortable_by = ('author', 'created', 'updated', 'title', 'category')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'body')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
