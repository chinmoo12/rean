from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/a/', views.post_list, name='post_a'),
    path('post/w/', views.post_list, name='post_w'),
    path('post/p/', views.post_list, name='post_p'),
    path('post/l/', views.post_list, name='post_l'),
    path('post/e/', views.post_list, name='post_e'),
    path('post/m/', views.post_list, name='post_m'),
    path('post/d/', views.post_list, name='post_d'),
    path('post/start/', views.post_list, name='post_start'),
]
