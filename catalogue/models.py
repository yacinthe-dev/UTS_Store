
from django.db import models
from django.utils import timezone

class Categorie(models.Model):
    nom=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True,default="")

    def __str__(self):
        return self.nom

#fin categorie

class Promotion(models.Model):
    TYPES_PROMO = (
        ('SOLDE','Soldes'),('REDUCTION','Reduction immediate'),('FIDELITE','Offre fidelite') 
    )
    titre = models.CharField(max_length=20,choices=TYPES_PROMO,default='REDUCTION')
    type_promo=models.CharField(max_length=20,choices = TYPES_PROMO,default='REDUCTION')
    taux_reduction=models.FloatField(default=0.0)
    date_debut=models.DateField(default=timezone.now)
    date_fin=models.DateField()
    est_active=models.BooleanField(default=True)

    def est_valide(self):
        aujourd_hui=timezone.now().date()
        if self.est_active and (self.date_debut<= aujourd_hui <= self.date_fin):
            return True
        else:
            return False

    def __str__(self):
        return f"{self.titre} (-{self.taux_reduction}%)"
    #fin definition promotion

class Produit(models.Model):
    Categorie=models.ForeignKey( Categorie,on_delete=models.CASCADE,
                                null=True, blank= True, related_name="Produits")
                            
    Promotion=models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="Produits"
    )
    nom=models.CharField(max_length=200)
    description=models.TextField(blank=True,default="")
    prix_achat=models.FloatField(default=0.0)
    prix_vente=models.FloatField(default=0.0)
    quantite_stock=models.IntegerField(default=0)
    seuil_alerte=models.IntegerField(default=5)
    image=models.ImageField(upload_to="produits/",blank=True,null=True)
    date_ajout=models.DateTimeField(auto_now_add=True)

    def est_en_stock_faible(self):
        if self.quantite_stock <= self.seuil_alerte:
            return True
        else:
            return False
#inspirer de comptoire
    def message_alerte_stock(self):
        if self.quantite_stock==0:
            return f"Rupture de stock : {self.nom}"
        elif self.est_en_stock_faible():
            return f"Stock bas : {self.nom}({self.quantite_stock} restants)"
        else:
            return f"En stock({self.quantite_stock} disponibles)"

    def calculer_prix_final(self): #calcul le prix du produit après promotion
        if self.Promotion is not None and self.promotion.est_valide():
            remise =(self.prix_vente * self.Promotion.taux_reduction) / 100.0
            return self.prix_vente - remise
        return self.prix_vente

    def calculer_marge_unitaire(self): #calcule le benefice sur produit vendu
        return self.calculer_prix_final() - self.prix_achat

    def retirer_stock(self,quantite): #retirer la quantite achetée du stock si dispo
        if quantite <= self.quantite_stock:
            self.quantite_stock = self.quantite_stock - quantite
            self.save()
            return True
        else:
            return False

    def __str__(self):
        return f"{self.nom} ({self.calculer_prix_final()} FCFA)"

#fin definition produit 
    




       


    
# Create your models here.
