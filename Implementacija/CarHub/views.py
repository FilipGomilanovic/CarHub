from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import *
from json import dumps

# from CarHub.forms import NewUserForm


# Create your views here.


def Test(request):
    # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStrana.html', {'imeSlike': 'carhublogo.png'})


def Ulogovan(request):
    # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStranaUlogovan.html')

def profilKorisnika(request):
    return render(request, 'profilKorisnika.html')

def konkretanOglasProdaja(request):
    return render(request, 'konkretanOglasProdaja.html')
def konkretanOglasRent(request):
    return render(request, 'konkretanOglasRent.html')

def urediProfil(request):
    # try:
    #     profil = Korisnik
    #
    #     context = {    #     }
        return render(request, 'urediProfil.html')
    # except Korisnik.DoesNotExist:
    #     raise Http404("Korisnik not found")

def PretragaOglasa(request):
    forma=pretragaOglasa(request.POST or None)
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    # print(niz)
    # print(brendovi_modeli)

    dataJSON = dumps(niz)
    context = {
        "data": dataJSON,
        "brendovi" : brendovi,
        "forma_pretraziOglas":forma
    }
    return render(request=request, template_name='pretragaOglasa.html', context = context)
def PretragaOglasaRent(request):
    forma=pretragaOglasaRent(request.POST or None)
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    # print(niz)
    # print(brendovi_modeli)

    dataJSON = dumps(niz)
    context = {
        "data": dataJSON,
        "brendovi" : brendovi,
        "forma_pretraziOglasRent":forma
    }
    return render(request=request, template_name='pretragaOglasaRent.html', context = context)

def postavljanjeOglasa(request):
    forma=PostavljanjeOglasa(request.POST,request.FILES)
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    # print(niz)
    # print(brendovi_modeli)

    dataJSON = dumps(niz)
    context = {
        "data": dataJSON,
        "brendovi" : brendovi,
        "forma_postaviOglas":forma
    }
    return render(request=request, template_name='testForme.html', context = context)


def registracija(request):
    form = KorisnikNoviForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("CarHub:pocetnaStranaUlogovan")

    form = KorisnikNoviForm()
    return render(request=request, template_name="registracijaProbaDjango.html", context={"register_form": form})
    # return render(request,"registracijaProbaDjango.html")



def pregledOglasa(request):
    return render(request, 'pregledOglasa.html')


def prijava(request):
     if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password) #moraju da se taguju
            if user is not None:
                login(request, user)
                messages.info(request, f"Ulogovani ste kao{username}.")
                return redirect("CarHub:pocetnaStranaUlogovan")
            else:
                messages.error(request, "Netacno ime ili lozinka.")
        else:
             messages.error(request, "Netacno ime ili lozinka.")
     form = AuthenticationForm()
     return render(request=request, template_name="prijavaProbaDjango.html", context={"login_form": form})


            

def logout(request):
    messages.info(request, "Uspesno ste izlogovani")
    return redirect("CarHub:pocetnaStrana")


