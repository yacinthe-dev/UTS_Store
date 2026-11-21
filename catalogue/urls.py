from django.urls import path
from . import views

urlpatterns = [
    path('', views.Catalogue, name='catalogue'),
]