from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='news-home'),
    path('article/', views.article, name='news-article'),
    path('list/', views.list, name='my-list')
]
