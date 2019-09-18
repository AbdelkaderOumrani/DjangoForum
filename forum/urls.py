from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages import views as pages_views
from posts import views as post_views

urlpatterns = [
    path('', pages_views.landing_page),
    path('posts/', include('posts.urls')),
    path('categories/', post_views.categories, name='categories'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
