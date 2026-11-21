from django.db import models
from django.utils import timezone
from comptes.models import Client
from catalogue.models import Produit


# début définition Commande
class Commande(models.Model):
    """Classe Commande"""
    STATUTS = (
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('ANNULEE', 'Annulée'),
    )

    client = models.ForeignKey(Client,on_delete=models.CASCADE,related_name="commandes" )
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    utiliser_fidelite = models.BooleanField(default=False)
    date_commande = models.DateTimeField(auto_now_add=True)

    def calculer_total_brut(self):
        """Additionne les sous-totaux de toutes les lignes de la commande."""
        total = 0.0
        for ligne in self.lignes.all():
            total = total + ligne.calculer_sous_total()
        return total

    def calculer_remise_fidelite(self):
        """Applique 5% de réduction si le client a au moins 100 points de fidélité."""
        if self.utiliser_fidelite and self.client.points_fidelite >= 100:
            return (self.calculer_total_brut() * 5.0) / 100.0
        return 0.0

    def calculer_total_net(self):
        """Renvoie le montant final à payer."""
        return self.calculer_total_brut() - self.calculer_remise_fidelite()

    def valider_commande(self):
        """Valide la commande, met à jour le stock et génère la facture."""
        if self.statut == 'VALIDEE':
            return False

        # Vérification de la disponibilité en stock
        for ligne in self.lignes.all():
            if ligne.quantite > ligne.produit.quantite_stock:
                return False

        # Décrémentation du stock
        for ligne in self.lignes.all():
            ligne.produit.retirer_stock(ligne.quantite)

        # Mise à jour des points de fidélité du client
        montant_net = self.calculer_total_net()
        if self.utiliser_fidelite and self.client.points_fidelite >= 100:
            self.client.points_fidelite = self.client.points_fidelite - 100
        self.client.ajouter_points(montant_net)

        # Validation de la commande
        self.statut = 'VALIDEE'
        self.save()

        # Création automatique de la facture
        numero = f"FACT-{timezone.now().strftime('%Y%m%d')}-{self.id}"
        Facture.objects.create(
            commande=self,
            numero_facture=numero,
            montant_total=montant_net
        )
        return True

    def __str__(self):
        return f"Commande n°{self.id} - {self.client.nom}"
# fin définition Commande


# début définition LigneCommande
class LigneCommande(models.Model):
    """Classe LigneCommande"""
    commande = models.ForeignKey(Commande , on_delete=models.CASCADE,related_name="lignes")#foreignkey clé qui relie la classe ligne commande à commande
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        """Enregistre le prix final du produit si le prix unitaire n'est pas encore défini."""
        if self.prix_unitaire == 0.0:
            self.prix_unitaire = self.produit.calculer_prix_final()
        super().save(*args, **kwargs)

    def calculer_sous_total(self):
        """Calcule le montant de la ligne (quantité * prix_unitaire)."""
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"
# fin définition LigneCommande


# début définition Facture
class Facture(models.Model):
    """Classe Facture"""
    commande = models.OneToOneField(Commande,on_delete=models.CASCADE,related_name="facture")
    numero_facture = models.CharField(max_length=50, unique=True)
    date_emission = models.DateTimeField(auto_now_add=True)
    montant_total = models.FloatField(default=0.0)

    def __str__(self):
        return f"Facture {self.numero_facture} - {self.montant_total} FCFA"
# fin définition Facture





# Create your models here.
