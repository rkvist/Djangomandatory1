from django.urls import path, include

from . import views

urlpatterns = [
    path('check_out/', views.check_out, name='check_out'),
    path('check_in/', views.check_in, name='check_in'),
]