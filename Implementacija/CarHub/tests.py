from django.contrib.auth.models import Group
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from .models import *

def create_oglas(kor, brend):
    model = Model.objects.create(brend=brend, naziv_modela="serija 5", godisteDo=2, godisteOd=1, carreviewlink='')
    return Oglas.objects.create(vlasnik_id= kor,tip = 'p', cena=1000, boost=0, karoserija='limuzina', model_idmodel=model, grad = '', kilometraza=0, godiste = 2010, snaga=100, opis = '')

def create_mod(username):
    kor = Korisnik(username=username, uloga="", slika="", kontakt_telefon="123")
    kor.set_password("Gijan12345")
    Group.objects.create(name = 'mod')
    group = Group.objects.get(name = 'mod')
    kor.save()
    kor.groups.add(group)
    return kor

class NekiTest(TestCase):

    def test_nesto_nesto(self):
        kor = create_mod("ognjen")
        # create_oglas(kor, 'BMW')
        response = self.client.get('')
        self.assertContains(response, "PRODAJ", html=True)


class NekiTest2(TestCase):

    def test_nesto_nesto2(self):
        kor = create_mod("ognjen")
        # create_oglas(kor, 'BMW')
        response = self.client.get('')
        self.assertContains(response, "IZNAJMI", html=True)


class NekiTest3(TestCase):

    def test_nesto_nesto3(self):
        kor = create_mod("ognjen")
        # create_oglas(kor, 'BMW')
        response = self.client.get('')
        self.assertContains(response, "PRODAJ", html=True)
