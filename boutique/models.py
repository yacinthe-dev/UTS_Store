from django.db import models


class Produit(models.Model):
    nom = models.CharField(max_length = 100)
    prix = models.FloatField()
    stock = models.IntegerField(default = 0)
    description = models.TextField(blank = True)
    seuil_alert = models.IntegerField(default = 5)

    def ajouter_produit(self):
        self.save()

    def afficher_produit(self):
        return f"{self.nom} - {self.prix} FCFA Stock : {self.stock}"

    def supprimer_produit(self):
        self.delete()
    @staticmethod
    def recheche_produit(nom_recherche):
        return Produit.objects.filter(nom__icontaint=nom_recherche)
    def __str__(self):
        return self.nom

# Create your models here.
