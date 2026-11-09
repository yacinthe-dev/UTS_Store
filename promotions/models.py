from django.db import models
from decimal import Decimal # pour calculer l'argent
from django.utils import timezone
from django.core.validators MinValueValiator, MaxValueValidator

class Promotion(models.Model):
    nom = models.CharField(max_length = 100)
    type_promo = models.CharField(max_length = 100)
    pourcentage = models.PositiveIntegerField(default = 1)
    debut_date = models.DateField()
    fin_date = models.DateField()
    active= models.BooleanField(default = True)
    produits = models.ManyToManyField(blank = True)
    categorie = models.ForeignKey('Categorie', on_delete=models= SET_NULL, null = True, blank = True)


    TYPE_CHOICES = [
          ('pourcentage', 'Pourcentage'), # exemple 10%
          ('montant_fixe', 'Montant fixe'), # exemple 2000FCFA
          ('fidelite', 'Fidelite - produit')
    ]
    def promotion_valide_pour_(self, produit):



    def prix_apres_promotion(self, produit):




    def palier_du_client(self, client):




    def calcul_total_commande(self, commande):



    def points_fidelite_gagnants(self, commande):
    def __str__(self):
            return f"Promotions {self.id}"
        
    # Create your models here.
