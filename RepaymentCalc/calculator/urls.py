from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.index, name='index'),
    path('calculate/', views.calculate_payments_simple, name='calculate'),
]