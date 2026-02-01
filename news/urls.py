from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('visitors/', views.visitors_map, name='visitors_map'),
    path('visitors/api/', views.visitors_api, name='visitors_api'),
]
