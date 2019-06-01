from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forum', views.dashboard, name='dashboard'),
]
