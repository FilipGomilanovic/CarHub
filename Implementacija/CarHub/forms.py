from cgitb import text

from dataclasses import field
from hashlib import new
from lib2to3.pgen2.token import NEWLINE
from logging import PlaceHolder
from tkinter.tix import Form
from tkinter.ttk import Style
from turtle import color

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ChoiceField, ModelForm
from django.utils.safestring import mark_safe

from .models import *


# kreiranje formi

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
        model = Korisnik  # moramo definisati da ne koristimo default User model, vec nas redefinisan
        fields = ("username", "email", "kontakt_telefon", "password1", "password2")


class PostavljanjeOglasa(forms.Form):
    CHOICES = [
        ('izbor', 'Izaberi karoseriju'),
        ('limuzina', 'Limuzina'),
        ('karavan', 'Karavan'),
        ('hedzbek', 'Hedzbek'),
        ('dzip', 'SUV')
    ]

    godiste = forms.IntegerField(label="Godiste:", required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Unesite godiste'}))
    kilometraza = forms.IntegerField(label="Kilometraza:", required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'Unesite kilometrazu'}))
    snagaMotora = forms.IntegerField(label="Snaga motora:", required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'Unesite snagu motora'}))
    karoserija = forms.ChoiceField(choices=CHOICES, required=True, initial=CHOICES[0])
    # slike = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))


class KomentarForm(ModelForm):
    class Meta:
        model = Komentar
        fields = ['sadrzaj']


class PorukaForm(ModelForm):
    class Meta:
        model = Poruke
        fields = ['sadrzaj']


class PromeniSliku(forms.Form):
    slika = forms.FileField(label="", widget=forms.FileInput(attrs={'placeholder': 'Izmeni profilnu sliku'}),
                            required=False)


class pretragaOglasa(forms.Form):
    CHOICES = [
        ('izbor', 'Izaberi karoseriju'),
        ('limuzina', 'Limuzina'),
        ('karavan', 'Karavan'),
        ('hedzbek', 'Hedzbek'),
        ('dzip', 'SUV')
    ]

    karoserija = forms.ChoiceField(choices=CHOICES, required=True, initial=CHOICES[0])
    godiste1 = forms.IntegerField(label="Godiste od:", required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Unesite godiste od'}))
    godiste2 = forms.IntegerField(label="Godiste do:", required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Unesite godiste do'}))
    cena1 = forms.IntegerField(label="Cena od:", required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Unesite cenu od'}))
    cena2 = forms.IntegerField(label="Cena do:", required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Unesite cenu do'}))


class pretragaOglasaRent(forms.Form):
    grad = forms.CharField(label="Grad", required=True, widget=forms.TextInput(attrs={'placeholder': 'Unesite grad'}))
    datumOd = forms.DateField(label="Datum od", required=False, input_formats=['%d-%m-%Y'],
                              widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Unesite datum od'}))
    datumDo = forms.DateField(label="Datum do", required=False, input_formats=['%d-%m-%Y'],
                              widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Unesite datum do'}))


class CetSearchForm(forms.Form):
    term = forms.CharField(max_length=50)