from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('posts/<int:pk>/<slug:post_slug>/', views.PostView.as_view(), name='post_detail'),
    path('posts/edit/<int:pk>/<slug:post_slug>/', views.PostEditView.as_view(), name='post_edit'),
    path('posts/delete/<int:pk>/<slug:post_slug>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/add', views.PostCreateView.as_view(), name='post_create'),
    path('like/<int:pk>/', views.PostLikeView.as_view(), name='like'),
]
