from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accueil = tableau_de_bord
    path('', include('tableau_de_bord.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('commande/', include('commande.urls')),
    path('compte/', include('comptes.urls')),
    path('promotion/', include('promotions.urls')),
    
]