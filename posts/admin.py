from django.contrib import admin
from .models import Category, Post, Comment, Attachment


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'description', 'created', 'updated', 'slug')


class PostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'category', 'status',
                    'created', 'updated', 'author')
    list_filter = ('status', 'category')
    search_fields = ('title', 'body')
    sortable_by = ('created', 'updated', 'title', 'category')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'body')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
