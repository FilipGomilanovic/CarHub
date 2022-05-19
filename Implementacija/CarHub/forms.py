
from dataclasses import field
from tkinter.tix import Form

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ChoiceField

from .models import *



#kreiranje formi

# class NewUserForm(UserCreationForm):
#     email=forms.EmailField(required=True)
#     number=forms.CharField(max_length=12, required=True)

#     class Meta:
#         model=User
#         fields=("username","email","number","password1","password2")

#         def __init__(self):

#          def save(self,commit=True):
#             user=super(NewUserForm,self).save(commit=False)
#             user.email=self.cleaned_data['email']
#             user.number=self.cleaned_data['number']
#             if commit:
#                 user.save()
#             return user



class KorisnikNoviForm(UserCreationForm):

    class Meta:
        model = Korisnik   #moramo definisati da ne koristimo default User model, vec nas redefinisan
        fields = ("username", "email", "kontakt_telefon", "password1", "password2")


def popuniIzbore(izbor):
    brendovi = Model.objects.values("brend").distinct()
    izbor.append(('default', 'Izaberite brend'))
    for brend in brendovi:
        izbor.append((str(brend), str(brend)))
    return izbor

class PostavljanjeOglasa(forms.Form):
    CHOICES = []
    CHOICES = popuniIzbore(CHOICES)

    brend = forms.ChoiceField(choices = CHOICES, required = True)
    model = forms.ChoiceField(choices=CHOICES, required=True)
    term = forms.CharField(max_length=100)


    # class Meta:
    #        #moramo definisati da ne koristimo default User model, vec nas redefinisan
    #     fields = ("brend", "naziv")