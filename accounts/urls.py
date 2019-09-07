from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('/', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.edit_profile, name='edit_profile'),
    path('profile', views.show_profile, name='show_profile'),
    path('profile/change_username', views.change_username, name='change_username'),
    path('profile/change_fullname', views.change_fullname, name='change_fullname'),
    path('profile/change_email', views.change_email, name='change_email'),
    path('profile/change_bio', views.change_bio, name='change_bio'),
    path('profile/change_avatar', views.change_avatar, name='change_avatar'),
    path('profile/change_password', views.change_password, name='change_password'),
    path('profile/deactivate_account',
         views.deactivate_account, name='deactivate_account'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activate'),
    # --------------------------------------------------
    re_path(r'^password_reset/$',
            auth_views.PasswordResetView.as_view(
                template_name='accounts/registration/password_reset_form.html'),
            name='password_reset'),
    re_path(r'^password_reset/done/$',
            auth_views.PasswordResetDoneView.as_view(
                template_name='accounts/registration/password_reset_done.html'),
            name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    re_path(r'^reset/done/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/registration/password_reset_complete.html'),
            name='password_reset_complete'),
]
