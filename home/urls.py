from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books, name='books'),
    path('magazines', views.magazines, name='magazines'),
    path('my_checkouts/', views.my_checkouts, name='my_checkouts'),
    path('expired_checkouts/', views.expired_checkouts, name='expired_checkouts'),
]