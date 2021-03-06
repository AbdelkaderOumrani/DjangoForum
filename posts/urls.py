from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:search_val>', views.search_posts, name="search_posts"),
    path('new_post', views.new_post, name='new_post'),
    path('', views.recent_posts, name='recent_posts'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('cat=<int:category_id>/<str:category_slug>', views.posts_by_category,
         name='posts_by_category'),
    path('<int:post_id>/<str:post_slug>', views.single_post,
         name='single_post'),
    path('delete_post/<int:post_id>', views.delete_post,
         name='delete_post'),
    path('edit_post/<int:post_id>', views.edit_post,
         name='edit_post'),
    path('add_new_comment/<int:post_id>', views.add_new_comment,
         name='add_new_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment,
         name='delete_comment'),

]
