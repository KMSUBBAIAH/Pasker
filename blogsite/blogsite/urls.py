"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name='register'),
    path('profile/',user_views.profile,name='profile'),
    # path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('login/',user_views.CustomLoginView.as_view(),name='login'),
    path('logout/',user_views.CustomLogoutView.as_view(),name='logout'),
    path('authentication/',user_views.authentication,name='authentication'),
    path('get-csrf-token/', user_views.get_csrf_token, name='get_csrf_token'),
    path('activate/<uidb64>/<token>/',user_views.activate, name='activate'),
     path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('', include('blogapp.urls')),
    # path('password-locker/', credential_views.view_protected_data, name='password_locker_view'),
    # path('password-locker/', password_locker_view, name='password_locker_view'),
    # path('add-credentials/', credential_views.add_credentials, name='add_credentials'),
    path('password-locker/', include('password_locker.urls')),
    # path('blog/', include('blogapp.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)