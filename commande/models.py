from django.db import models
from comptes.models import Client
from catalogue.models import Produit

class Commande(models.Model):
    #statuts possible de la commande
    STATUS = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('anulee', 'Annulée'),
    ]
    client = models.ForeignKey(Client, on_delete= models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete= models.CASCADE)
    quantite = models.IntegerField(default = 1)
    date_commande = models.DateTimeField(auto_now_add= True)
    statut = models.CharField(max_length= 20, choices= STATUS, default= 'en_attente')


    #client
    def ajouter_commande(self):
        self.save()

    def voir_facture(self):
        total= self.produit.prix*self.quantite
        return f"Facture {self.id} - {self.client.nom} - Total: {total} FCFA"

    def payer(self):
        self.statut= 'payee'
        self.save()

    #Admin
    def afficher_commande(self):
        return f"Commande {self.id} {self.client.email} - {self.statut}"

    def modifier_statut(self, nouveau_statut):
        self.statut= nouveau_statut
        self.save()

    def supprimer_commande(self):
        self.delete()

    def supprimer_fature(self):
        total = self.produit.prix*self.quantite
        return {
            'numero': f"FACT-{self.id}",
            'client': self.client.email,
            'quantite': self.produit.nom,
            'total': total,
        }
    @staticmethod
    def recherche_commande(email_client):
        return Commande.objects.filter(client__email__icontains= email_client)

    def __str__(self):
        return f"Commande {self.id}"



class ligneCommande(models.Model):
    quantite = models.IntegerField(default = 1)
    prix_initaire = models.IntegerField(default = 1)
    commande = models.CharField(max_length = 100)  # chaque facture apartient a un comande
    produit = models.IntegerField(default = 1)





class Facture(models.Model):
    date_facture = models.DateTimeField(default = 1)
    montant_total = models.IntegerField(default = 1)
    commande = models.CharField(max_length = 100)  # chaque facture apartient a un comande
    
    

# Create your models here.
