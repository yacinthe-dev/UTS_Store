from email.policy import default

from django.db import models
"""classe utilisateur pour l'inscription et la connexion"""


class Client(models.Model):
    nom = models.CharField(max_length = 100)
    prenom = models.CharField( max_length = 100)
    adresse = models.CharField(max_length = 100)
    email = models.CharField(unique = True)
    tel = models.CharField(max_length = 10)
    est_vendeur = models.BooleanField(default= False)
    mot_de_passe = models.CharField(max_length = 255)


    # 2. gestion du profil du client
    def affiche_profil(self):
      # affichage du profil

      return f"{self.nom} - {self.prenom} - {self.tel} - {self.email} - {self.adresse}"

    def modifier_profil(self, nouveau_tel, nouveau_add, nouveau_nom, nouveau_prenom, ):
      self.tel = nouveau_tel
      self.adresse = nouveau_add
      self.nom = nouveau_nom
      self.prenom = nouveau_prenom
      self.save()
    def supprimer_profil(self):
        # supprimer ce client de la base
        self.delete()

    # 4. gestion du client
    def affiche_client(self):
              # affichage du client
        
              return f" {self.tel} - {self.email} - {self.tel}"
        
    def modifier_client(self, nouveau_tel, nouveau_add,  ):
              self.tel = nouveau_tel
              self.adresse = nouveau_add
              self.save()
    def supprimer_client(self):
                # supprimer ce client de la base
                self.delete()

    @staticmethod
    def recherche(email_recherche):
           return Client.objects.filter(email__icontaints= email_recherche)
        
    def __str__(self):
              return self.email
    

class HistoriqueCommande(models.Model):
      client = models.ForeignKey(Client, on_delete= models.SET_NULL, null = True )
      produit = models.CharField(max_length = 100)
      date_achat = models.DateTimeField(auto_now_add= True)
      montant = models.FloatField()

      def __str__(self):
            return f"{self.client.email} - {self.produit} - {self.date_achat} - {self.montant}"

class Connexion(models.Model):
        """classe connexion"""
        email = models.EmailField(unique = True)
        mot_de_passe = models.CharField(max_length = 255)

# Create your models here.
