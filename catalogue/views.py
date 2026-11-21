from django.shortcuts import render

from .models import Produit

def Catalogue(request):
    q = request.GET.get('q','')

    if q:
        produits = Produit.rechecher_produit(q)
    else:
        produits = Produit.objects.all()

    return render(request, 'posts/catalogue.html', {
        'produits': produits,
        'q': q,
    })
# Create your views here.
