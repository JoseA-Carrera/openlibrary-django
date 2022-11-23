from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='books'),
    path('authors/', views.authors, name='authors')
]