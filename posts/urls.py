from django.urls import path
from . import views

urlpatterns = [
    path('new_post', views.new_post, name='new_post'),
    path('', views.recent_posts, name='recent_posts'),
    path('cat(?)<str:category_slug>', views.posts_by_category,
         name='posts_by_category'),
    path('<int:post_id>/<str:post_slug>', views.single_post,
         name='single_post'),
]
