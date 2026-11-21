

from django.db import models
from django.utils import timezone

class Promotion(models.Model):
    # Nom de la promotion visible dans l'interface et les filtres
    nom = models.CharField(max_length=255)

    # Indique si la promotion est active ou non
    active = models.BooleanField(default=True)

    # Date de début de validité de la promotion
    date_debut = models.DateField()

    # Date de fin de validité de la promotion
    date_fin = models.DateField()

    # Pourcentage de réduction appliqué si le type est "pourcentage"
    pourcentage_reduction = models.DecimalField(max_digits=5, decimal_places=2)

    # Type de promotion : pourcentage ou montant fixe
    type_promotion = models.CharField(
        max_length=50,
        choices=[('pourcentage', 'Pourcentage'), ('montant', 'Montant')],
    )

    # Produit concerné par cette promotion
    produit = models.ForeignKey('catalogue.produit', on_delete=models.CASCADE)

    # Catégorie concernée par cette promotion (optionnelle)
    categorie = models.ForeignKey('catalogue.categorie', on_delete=models.CASCADE, blank=True, null=True)

    # Ajoute une nouvelle promotion dans la base de données.
    def ajouter(self):
        self.save()

    # Modifie les champs de la promotion et sauvegarde les changements.
    def modifier(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    # Supprime la promotion de la base de données.
    def supprimer(self):
        self.delete()

    # Recherche les promotions dont le nom contient le texte donné.
    @classmethod
    def recherche(cls, nom_recherche):
        return cls.objects.filter(nom__icontains=nom_recherche)

    # Retourne True si la promotion est actuellement active.
    def est_en_cours(self):
        today = timezone.now().date()
        return self.date_debut <= today <= self.date_fin

    # Retourne True si la date actuelle est supérieure à la date de fin.
    def est_expire(self):
        today = timezone.now().date()
        return today > self.date_fin

    # Vérifie si une promotion existe et est active pour un produit donné.
    @classmethod
    def promotion_valide_pour_produit(cls, produit):
        today = timezone.now().date()
        return cls.objects.filter(produit=produit, date_debut__lte=today, date_fin__gte=today).exists()

    # Calcule le nouveau prix après application de la réduction.
    def prix_apres_promotion(self, prix_initial):
        if self.type_promotion == 'pourcentage':
            # Exemple : 20% de réduction
            return prix_initial * (1 - self.pourcentage_reduction / 100)
        elif self.type_promotion == 'montant':
            # Exemple : réduction de 500F sur le prix
            return max(0, prix_initial - self.pourcentage_reduction)
        return prix_initial

    # Alias simple pour vérifier si la promotion est active.
    def est_active(self):
        today = timezone.now().date()
        return self.date_debut <= today <= self.date_fin

    # Représentation textuelle de la promotion dans l'administration Django.
    def __str__(self):
        return self.nom


# Create your models here.