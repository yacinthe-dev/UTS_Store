from django.urls import path
from.import views

urlpatterns = [
    path('', views.Accueil, name='accueil'),
    path('catalogue/', views.Catalogue, name='catalogue'),
    path('commande/', views.Commande, name='commande'),
    path('promotions/', views.Promotion, name='promotions'),
    
    
    path('compte/', views.Compte, name='compte'),
    path('connexion/', views.Connexion, name='connexion'),
    path('inscription/', views.InscriptionEtape1, name='inscription'),
    path('inscription/etape2/', views.InscriptionEtape2, name='inscription_etape2'),
    path('deconnexion/', views.Deconnexion, name='deconnexion'),

    
]