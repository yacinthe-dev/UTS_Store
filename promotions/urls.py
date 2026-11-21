from django.urls import path
from . import views

urlpatterns = [
    path('', views.promotions, name='promotions'),
]