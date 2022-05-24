
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
from django.forms import ChoiceField
from django.utils.safestring import mark_safe



from .models import *


class KorisnikNoviForm(UserCreationForm):

    class Meta:
        model = Korisnik   #moramo definisati da ne koristimo default User model, vec nas redefinisan
        fields = ("username", "email", "kontakt_telefon", "password1", "password2")


class PostavljanjeOglasa(forms.Form):
 
    CHOICES=[
        ('izbor','Izaberi karoseriju'),
        ('limuzina','Limuzina'),
        ('karavan','Karavan'),
        ('hedzbek','Hedzbek'),
        ('dzip','SUV')
    ]

   
    godiste = forms.IntegerField(label="Godiste:", required=False,widget=forms.TextInput(attrs={'placeholder':'Unesite godiste'}))
    kilometraza = forms.IntegerField(label="Kilometraza:", required=False,widget=forms.TextInput(attrs={'placeholder':'Unesite kilometrazu'}))
    snagaMotora = forms.IntegerField(label="Snaga motora:", required=False,widget=forms.TextInput(attrs={'placeholder':'Unesite snagu motora'}))
    karoserija = forms.ChoiceField(choices=CHOICES,required=True,initial=CHOICES[0])
    slike = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
   
class PromeniSliku(forms.Form):
    slika = forms.FileField(widget=forms.FileInput(attrs={'multiple': False}))
    
