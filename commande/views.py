from django.shortcuts import render


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Commande
from catalogue.models import Produit
from comptes.models import Client

# ---------- CLIENT ----------

@login_required
def ajouter_commande(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    # Ton client est lié à l'email de l'utilisateur connecté
    client = get_object_or_404(Client, email=request.user.email)

    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        commande = Commande(client=client, produit=produit, quantite=quantite)
        commande.ajouter_commande()  # ta méthode du modèle

        # Diminue le stock
        produit.quantite = produit.quantite - quantite
        produit.save()
        return redirect('voir_facture', commande_id=commande.id)

    return render(request, 'commande/ajouter.html', {'produit': produit})

@login_required
def mes_commandes(request):
    client = get_object_or_404(Client, email=request.user.email)
    commandes = Commande.objects.filter(client=client)
    return render(request, 'commande/mes_commandes.html', {'commandes': commandes})

@login_required
def voir_facture(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    facture = commande.generer_facture()  # ta méthode
    return render(request, 'commande/facture.html', {'commande': commande, 'facture': facture})

@login_required
def payer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.payer()  # ta méthode : statut -> 'payee'
    return redirect('voir_facture', commande_id=commande.id)

# ---------- ADMIN ----------

def liste_commandes(request):
    q = request.GET.get('q', '')
    if q:
        commandes = Commande.recherche_commande(q)  # ta méthode static
    else:
        commandes = Commande.objects.all()
    return render(request, 'commande/liste.html', {'commandes': commandes, 'q': q})

def modifier_statut(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        nouveau = request.POST.get('statut')
        commande.modifier_statut(nouveau)  # ta méthode
        return redirect('liste_commandes')
    return render(request, 'commande/modifier_statut.html', {'commande': commande})

def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.supprimer_commande()  # ta méthode
    return redirect('liste_commandes')
# Create your views here.
