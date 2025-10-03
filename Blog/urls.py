from django.urls import path
from . import views
from .views import posts_view, PostDetail

app_name = 'blog'

urlpatterns = [
    path('posts/', posts_view, name='posts'),
    path('details/<int:pk>/', PostDetail.as_view(), name='post_detail'), 
]