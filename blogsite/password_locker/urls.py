from django.urls import path
from password_locker.views import *

urlpatterns = [
    path('credentials-page/', CredentialListView.as_view(), name='credentials_view'),
    path('credentials-page/<int:pk>/', detail_credential, name='credential-detail'),
    path('credentials-page/new/', create_credential, name='credential-create'),
    path('credentials-page/<int:pk>/update/', update_credential, name='update-credential'),
    path('credentials-page/<int:pk>/delete/', delete_credential, name='delete-credential'),
]
