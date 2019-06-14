from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profil/edit', views.edit_profil, name='edit_profil'),
]
