from django import forms
class Etape1Form(forms.Form):
    nom= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class Etape2Form(forms.Form):
    adresse= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tel= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mot_de_passe= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    est_vender= forms.BooleanField(required=False, label='Je suis vendeur ?')