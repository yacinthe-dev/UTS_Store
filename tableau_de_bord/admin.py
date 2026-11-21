from django.contrib import admin
from .models import resume, alerte_stock, produit_populaire

@admin.register(resume) #enregistrer resumé dans l'admi
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('date', 'nombre_commandes', 'nouveau_clients', 'chiffre_affaire', 'promotions_utilise','date_creation')
    list_filter = ('date', 'date_creation',) #filtre la date
    search_fields = ('date',)
    readonly_fields = ('date', 'date_creation',) # on ne modifie pas la date a la main

@admin.register(alerte_stock)
class AlerteStockAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_alerte', 'est_active', 'message',)
    list_filter = ('type_alerte', 'est_active') #filtre les alertes actives
    search_fields = ('titre', 'message',)
    list_editable = ('est_active',) # active/desactive depuis la liste

@admin.register(produit_populaire)
class ProduitPopulaireAdmin(admin.ModelAdmin):
    list_display = ('produit', 'total_vendu', 'chiffre_affaire_genere',)
    ordering = ('-total_vendu',) #on trie les plus vendu
    search_fields = ('produit',)
    

    



# Register your models here.
