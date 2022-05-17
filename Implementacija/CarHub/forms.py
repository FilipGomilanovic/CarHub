
from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



#kreiranje formi

# class NewUserForm(UserCreationForm):
#     email=forms.EmailField(required=True)
#     number=forms.CharField(max_length=12, required=True)
#
#     class Meta:
#         model=User
#         fields=("username","email","number","password1","password2")
#
#         def __init__(self):
#
#         def save(self,commit=True):
#             user=super(NewUserForm,self).save(commit=False)
#             user.email=self.cleaned_data['email']
#             user.number=self.cleaned_data['number']
#             if commit:
#                 user.save()
#             return user


class KorisnikNovi(forms.Form):
    username = forms.CharField(max_length=36, required=True)
    password = forms.CharField(max_length=36, required=True)
    number= forms.CharField(max_length=12, required=True)
    email = forms.EmailField(required=True)

