from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from .models import resume, alerte_stock, produit_populaire
from commande.models import Commande
from commande.models import Client
from .forms import Etape1Form, Etape2Form


# Page principale: Le Tableau de bord
def Accueil(request):
    # 1. Top 5
    top_5 = produit_populaire.top_produit_vendu()

    # 2. Totaux produits populaires
    total_vendu = 0
    chiffre_total = 0
    for p in produit_populaire.objects.all():
        total_vendu = total_vendu + p.total_vendu
        chiffre_total = chiffre_total + p.chiffre_affaire_genere

    # 3. Dernier résumé du jour (nombre_commandes, nouveaux clients...)
    dernier_resume = resume.objects.order_by('-date').first()

    # 4. Alertes actives
    alertes = alerte_stock.objects.filter(est_active=True)

    return render(request, 'posts/index.html', {
        'top_5': top_5,
        'total_vendu': total_vendu,
        'chiffre_total': chiffre_total,
        'dernier_resume': dernier_resume,
        'alertes': alertes,
    })

def Catalogue(request):
    return render(request, 'posts/catalogue.html')

def Commande(request):
    return render(request, 'posts/commande.html')

def Compte(request):
    return render(request, 'posts/compte.html')

def Promotion(request):
    return render(request, 'posts/promotion.html')

def liste_alertes(request): #voire tous es alertes
        alertes = alerte_stock.objects.all().order_by('-id')
        return render(request, 'tableau_de_bord/index.html', {'alertes': alertes})

def liste_produit_populaires(request):
        produits = produit_populaire.objects.all().order_by('-total_vendu')
        return render(request, 'tableau_de_bord/produits.html', {'produits'})

def InscriptionEtape1(request):
     if request.method== 'POST':
        form = Etape1Form(request.POST) # on met ce que la personne a tapé dans le formulaire
        if form.is_valid(): #django verifie si les cases sont pas vide
             request.session['inscription_nom']= form.cleaned_data['nom'] # garde ces infos en memoire temporaire
             request.session['inscription_prenom']= form.cleaned_data['prenom']  

             return redirect('inscription_etape2')
        else:
             form = Etape1Form()
        #envoyé la formulaire a html pour l'afficher
        return render(request,'posts/inscription_etape1.html', {'form': form})
             
def InscriptionEtape2(request):
     if 'inscription_nom' not in request.session: #si la personne saute l'etape 1
          return redirect('inscription_etape1')
     if request.method == 'POST':
        form = Etape2Form(request.POST) # on met ce que la personne a tapé dans le formulaire
        if form.is_valid(): #django verifie si les cases sont pas vide
                  client = Client( 
                     nom=request.session['inscription_nom'],
                     prenom=request.session['inscription_prenom'],
                     adresse=form.cleaned_data['adresse'],
                     email=form.cleaned_data['email'],
                     tel=form.cleaned_data['tel'],
                     est_vender=form.cleaned_data['est_vender'],
                     mot_de_passe=make_password(form.cleaned_data['email']) #le mot de passe n'est pas enregistrer en clair

                  )
                  client.save()
                  del request.session['inscription_nom'],
                  del request.session['inscription_prenom'],
                  return redirect('connexion')
     
     else :
              form = Etape2Form()                   
     

     return render(request, 'posts/inscription_etape2.html', {'form': form})

def Compte(request):
     client_id = request.session.get('client_id') # verifier si la personne est connecté
     if not client_id:
          return redirect('connexion')

     client = Client.objects.get(id=client_id)
     return render(request, 'posts/compte.html', {'client': client})

def Connexion(request):
     erreur=None #pour ne pas afficher erreur si la personne vient d'arrivé
     if request.method == 'POST':
          email = request.POST.get('email')
          mot_de_passe = request.PORT.get('mot_de_passe')
          try:
               client = Client.objects.get(email=email)
               if check_password(mot_de_passe, client.mot_de_passe):
                    request.session['client_id']= client.id
                    request.session['client_nom']= client.nom
                    return redirect('compte')
               else:
                    erreur= "Mot de passe ou email incorect."
          except Client.DoesNotExist: # si on ne trouve pas l'email
               erreur = "Ce email n'existe pas. Inscrivez vous d'abord."
     return render(request, 'posts/connexion.html', {'erreur': erreur})

def Deconnexion(request):
     request.session.flush()
     return redirect('connexion')
     
    
    


# Create your views here.
