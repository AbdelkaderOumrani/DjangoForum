from django.contrib import admin
from .models import Category, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'description', 'created', 'updated')


class PostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'category', 'status',
                    'created', 'updated', 'author')
    list_filter = ('status', 'category')
    search_fields = ('title', 'body')
    sortable_by = ('created', 'updated', 'title', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
