from django.db import models
from commande.models import Commande, ligneCommande, Facture

class resume (models.Model):
    date = models.DateTimeField(auto_now_add= True)
    nombre_commandes = models.IntegerField(default = 0)
    nouveau_clients = models.IntegerField(default = 0)
    chiffre_affaire = models.IntegerField(default = 0)
    promotions_utilise = models.IntegerField(default = 0)
    date_creation = models.DateTimeField(auto_now_add= True)

    def compter_commandes(debut, fin):
        return Commande.objects.filter( statut= "payee", date_commande__range=(debut, fin)).count()

    def calculer_chiffre_affaire(debut, fin): # calcul du chiffre d'affaire des commandes payée entre deux dates
        factures = Facture.objects.filter( commande__statut = "payee",
                                          commande__date_commande__date__range=(debut, fin))
        resultat = factures.aggregate(total=models.Sum(models.F('commande__produit__prix') * models.F('commande__quantite')))['total']

        return resultat
    
    def compte_nouveaux_clients(self):
        self.nouveau_clients = self.client_set.count() # enregistrer la nouvelle valeur dans la base de données
        self.save()

    def compter_promotions_utilisees(self):
        self.promotions_utilise = self.promotions.set.count()
        self.save()

    def affiche_graphique(self):
        # code pour générer un graphique à partir des données du résumé
        pass


class alerte_stock(models.Model):
    titre = models.CharField(max_length = 100)
    message = models.TextField()
    type_alerte = models.CharField(max_length = 100)
    est_active = models.BooleanField(default = True)

    def message_alerte(self):
        return f"{self.titre} - {self.message} - {self.type_alerte} - {'Active' if self.est_active else 'Inactive'}"


# Create your models here.
