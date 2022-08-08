from django.urls import path
from . import views

urlpatterns = [
    path('', views.shortener, name='shortener'),
    path('<new_url>/', views.original, name='original'),
]
