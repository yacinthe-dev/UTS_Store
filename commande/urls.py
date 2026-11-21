from django.urls import path
from . import views

urlpatterns = [
    path('', views.commande, name='commande'),
]