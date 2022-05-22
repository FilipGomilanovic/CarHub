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



def konkretanOglasProdaja(request, oglas_id):
    #namestiti
    oglas = Oglas.objects.get(pk = oglas_id)
    model_oglasa = oglas.model_idmodel
    lista_slika = list(Slike.objects.filter(fk_oglas=oglas))
    print(lista_slika[0].slike)
    #slika1 = lista_slika[0]
    oglas_dict = {
        'brend' : model_oglasa.brend,
        'model' : model_oglasa.naziv_modela,
        'cena' : oglas.cena,
        'boost' : oglas.boost,
        'slike' : lista_slika,
        'snaga' : oglas.snaga,
        'kilometraza' : oglas.kilometraza,
        'godiste' : oglas.godiste,
        'karoserija' : oglas.karoserija,
    }

    return render(request, 'konkretanOglasProdaja.html', context={'oglas' : oglas_dict})



def konkretanOglasRent(request):
    #namestiti
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
    form=PostavljanjeOglasa(request.POST or None,request.FILES or None)
    if form.is_valid():
        izbor = request.POST['izbor']
        brend = request.POST['dropdown_Brend']
        naziv_model = request.POST['dropdown_Model']
        godiste = form.cleaned_data.get('godiste')
        kilometraza = form.cleaned_data.get('kilometraza')
        snaga = form.cleaned_data.get('snagaMotora')
        karoserija = form.cleaned_data.get('karoserija')
        slike = request.FILES.getlist('images')

        model_id = Model.objects.filter(godisteOd__lte=godiste).filter(godisteDo__gte=godiste).filter(
            brend=brend).filter(naziv_modela=naziv_model)  #filtriranje radi pronalaska id-ja modela
        #print(model_id)
        #proveriti sta vraca post request za izbor (da li vraca value od pritisnitog dugmeta)
        if (izbor == "prodaja"):
            cena = request.POST["cenaProdaja"];
            for img in slike:
                print(img)
            oglas = Oglas(tip = "p", cena = cena, boost = 0, grad = '', slike = slike,
                          snaga = snaga, kilometraza=kilometraza, karoserija=karoserija,
                          godiste=godiste, model_idmodel=model_id.first())
            oglas.save()
            for img in slike:
                photo = Slike.objects.create(slike = img, fk_oglas = oglas)
        else:
            pass
        #napraviti razlicite ifove za prodaju i iznajmljivanje
        #ako je prodaja, moze odmag da se postavi oglas
        #ako je iznajmljivanje, treba smisliti nacin za kupljenje datuma i za njihovubacivanje u bazu
        #takodje, mora se naci id_Modela pomocu brenda, modela i godista

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
        "forma_postaviOglas":form
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


