from django.urls import path, include
from .views import PostListView,PostCreateView, PostDeleteView, PostDetailView, PostUpdateView, UserPostListView
from . import views
from password_locker import views as credential_views

urlpatterns = [
    path('',views.base,name='blog-base'),
    path('home/',PostListView.as_view(),name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('about/',views.about,name='blog-about'),
]