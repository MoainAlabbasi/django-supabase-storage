"""
URL Configuration لتطبيق Storage
"""
from django.urls import path
from . import views

urlpatterns = [
    # Web Interface URLs
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),
    path('file/<int:pk>/delete/', views.delete_file, name='delete_file'),
    
    # API URLs
    path('api/files/', views.api_list_files, name='api_list_files'),
    path('api/files/<int:pk>/', views.api_file_detail, name='api_file_detail'),
    path('api/upload/', views.api_upload_file, name='api_upload_file'),
    path('api/files/<int:pk>/delete/', views.api_delete_file, name='api_delete_file'),
]
