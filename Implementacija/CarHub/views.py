from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import register

from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import *
from json import dumps
import datetime
from datetime import datetime
from django import template

# from CarHub.forms import NewUserForm


# Create your views here.

@register.filter
def index(sequence, position):
    return sequence[position]

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
        'opis' : oglas.opis
    }

    return render(request, 'konkretanOglasProdaja.html', context={'oglas' : oglas_dict})



def konkretanOglasRent(request, oglas_id):
    poruka = ""
    datumi = []
    if request.method == "POST":
        datumOd = request.POST['start']
        datumDo = request.POST['end']
        datumOd = datetime.strptime(datumOd, '%Y-%m-%d').date()
        datumDo = datetime.strptime(datumDo, '%Y-%m-%d').date()
        print(type(datumOd))
        oglas = Oglas.objects.get(pk=oglas_id)
        datumi = list(Datumi.objects.filter(fk_oglas=oglas))
        print(datumi)
        fleg = True
        for datum in datumi:
            if (not (datumOd > datum.datumDo or datumDo < datum.datumOd)):
                fleg = False;
        if fleg == True:
            poruka = "Uspesno rezervisan termin!"
            dat = Datumi(datumOd=datumOd, datumDo=datumDo, fk_oglas=oglas)
            dat.save()
        else:
            poruka = "Datum je vec rezevisan!"

    oglas = Oglas.objects.get(pk=oglas_id)
    model_oglasa = oglas.model_idmodel
    lista_slika = list(Slike.objects.filter(fk_oglas=oglas))
    datumPocetni = datetime.now()
    datumPocetni = datumPocetni.strftime("%Y-%m-%d")

    #print(datumPocetni)
    oglas_dict = {
        'brend': model_oglasa.brend,
        'model': model_oglasa.naziv_modela,
        'cena': oglas.cena,
        'slike': lista_slika,
        'karoserija': oglas.karoserija,
        'godiste': oglas.godiste,
        'datumDanasnji' : datumPocetni,
        'poruka' : poruka
    }

    return render(request, 'konkretanOglasRent.html', context=oglas_dict)




def urediProfil(request):
    # try:
    #     profil = Korisnik
    #
    #     context = {    #     }
        return render(request, 'urediProfil.html')
    # except Korisnik.DoesNotExist:
    #     raise Http404("Korisnik not found")



def PretragaOglasa(request):

    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    poruka = ""
    forma=pretragaOglasa(request.POST or None)
    if forma.is_valid():
        brend = request.POST['dropdown_Brend']
        naziv_model = request.POST['dropdown_Model']
        godiste1 = forma.cleaned_data.get('godiste1')
        godiste2 = forma.cleaned_data.get('godiste2')
        karoserija = forma.cleaned_data.get('karoserija')
        cenaOd = forma.cleaned_data.get('cena1')
        cenaDo = forma.cleaned_data.get('cena2')
        # print(brend)
        # print(naziv_model)
        oglasi = []
        imgs = []

        models_ids = Model.objects.filter(godisteDo__gte=godiste2).filter(godisteOd__gte=godiste1).filter(
            brend=brend).filter(naziv_modela=naziv_model)
        print(models_ids)
        for model in models_ids:
            oglasi.extend(list(Oglas.objects.filter(model_idmodel=model).filter(godiste__lte=godiste2).filter(godiste__gte=godiste1).filter(karoserija=karoserija).filter(cena__gte=cenaOd).filter(cena__lte=cenaDo).filter(tip="p")))
        print(oglasi)

        if len(oglasi) != 0:
            for oglas in oglasi:
                nesto = Slike.objects.filter(fk_oglas=oglas)
                imgs.append(nesto.first().slike)
                #imgs.append((Slike.objects.filter(fk_oglas=oglas)).first().slike)
                print(imgs)
        else:
            poruka = "Nema oglasa!"
        dataJSON = dumps(niz)
        context = {
            "naziv_brenda" : brend,
            "naziv_modela" : naziv_model,
            "slike" : imgs,
            "oglasi" : oglasi,
            "data": dataJSON,
            "brendovi": brendovi,  #sluzi za padajucu listu
            "forma_pretraziOglas": forma,
            "poruka" : poruka
        }

        return render(request=request, template_name='pretragaOglasa.html', context = context)


    #ako je korisnik poslat na stranicu pretrage preko get requesta, to znaci da je to prvi ulaz tu,
    #a ako je preko post requesta, onda je vec napravio filtere i primenio ih
    #U slucaju da korisnik dolazi na sajt get requestom, pravi se lista od pocetnih 9 oglasa(boostovani, ili svi boos
    # tovani sa skrolom), a u slucaju da se dolazi na sajt nakon post requesta, onda se primenjuju filteri i
    #salju odgovarajuci oglasi

    #ovde ide kod za dobijanje boostovanih oglasa i njihovo slanje nakon GET request-a
    oglasi = []
    imgs = []
    brend_model = [] #lista naziva brenda i modela koju saljem kroz kontekst u slucaju da je get metod
    oglasi.extend(list(Oglas.objects.filter(boost=1)))

    print("pretraga oglasa - GET")

    if len(oglasi) != 0:
        for oglas in oglasi:
            model = Model.objects.get(idmodel=oglas.model_idmodel.idmodel)
            brend_model.append(str(model.brend) + " " + str(model.naziv_modela))
            nesto = Slike.objects.filter(fk_oglas=oglas)
            imgs.append(nesto.first().slike)
    else:
        poruka = "Nema oglasa!"

    dataJSON = dumps(niz)
    context = {
        "naziv_brenda_modela_list" : brend_model,
        "slike" : imgs,
        "oglasi" : oglasi,
        "data": dataJSON,
        "brendovi" : brendovi,     #za padajucu listu
        "forma_pretraziOglas":forma,
        "poruka" : poruka
    }
    return render(request=request, template_name='pretragaOglasa.html', context = context)


def PretragaOglasaRent(request):
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    poruka = ""
    form = pretragaOglasaRent(request.POST or None)
    if form.is_valid():
        grad = form.cleaned_data.get("grad")
        datumOd = form.cleaned_data.get("datumOd")
        datumDo = form.cleaned_data.get("datumDo")
        brend = request.POST['dropdown_Brend']
        naziv_model = request.POST['dropdown_Model']
        oglasi_pom = []
        models_ids = Model.objects.filter(brend=brend).filter(naziv_modela=naziv_model)
        for model in models_ids:
            oglasi_pom.extend(list(Oglas.objects.filter(grad=grad).filter(tip="r")))
        print(oglasi_pom)
        oglasi = []
        imgs = []


        if len(oglasi_pom) != 0:
            if datumOd != None and datumDo != None:
                for oglas in oglasi_pom:
                    datumi = list(Datumi.objects.filter(fk_oglas=oglas))
                    fleg = True;
                    for datum in datumi:
                        print(datum.datumOd.strftime("%d-%m-%y"))
                        print(datumOd.strftime("%d-%m-%y"))
                        if (not(datumOd.strftime("%d-%m-%y") > datum.datumDo.strftime("%d-%m-%y") or datumDo.strftime("%d-%m-%y") < datum.datumOd.strftime("%d-%m-%y"))):
                            fleg = False;
                    if fleg == True:
                        oglasi.append(oglas)

                for oglas in oglasi:
                    nesto = Slike.objects.filter(fk_oglas=oglas)
                    imgs.append(nesto.first().slike)
                    # imgs.append((Slike.objects.filter(fk_oglas=oglas)).first().slike)
                    print(imgs)
            else:
                oglasi = oglasi_pom
                for oglas in oglasi:
                    nesto = Slike.objects.filter(fk_oglas=oglas)
                    imgs.append(nesto.first().slike)
                print(oglasi)
        else:
           poruka = "Nema oglasa!"
        dataJSON = dumps(niz)
        context = {
            "naziv_brenda" : brend,
            "naziv_modela" : naziv_model,
            "oglasi" : oglasi,
            "data" : dataJSON,
            "brendovi" : brendovi,
            "forma_pretraziOglasRent": form,
            "slike" : imgs,
            "poruka" : poruka
        }

        return render(request=request, template_name='pretragaOglasaRent.html', context=context)

    oglasi = []
    imgs = []
    brend_model = []  # lista naziva brenda i modela koju saljem kroz kontekst u slucaju da je get metod
    oglasi.extend(list(Oglas.objects.filter(tip='r')))
    print("pretraga oglasa - GET")

    if len(oglasi) != 0:
        for oglas in oglasi:
            model = Model.objects.get(idmodel=oglas.model_idmodel.idmodel)
            brend_model.append(str(model.brend) + " " + str(model.naziv_modela))
            nesto = Slike.objects.filter(fk_oglas=oglas)
            imgs.append(nesto.first().slike)
    else:
        poruka = "Nema oglasa!"

    dataJSON = dumps(niz)
    context = {
        "naziv_brenda_modela_list": brend_model,
        "slike": imgs,
        "oglasi": oglasi,
        "data": dataJSON,
        "brendovi" : brendovi,
        "forma_pretraziOglasRent":form,
        "poruka" : poruka
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
            cena = request.POST["cenaIznajmljivanje"];
            grad = request.POST["Grad"]
            oglas = Oglas(tip = "r", cena = cena, boost = 0, grad = grad, slike = slike,
                          snaga = snaga, kilometraza=kilometraza, karoserija=karoserija,
                          godiste=godiste, model_idmodel=model_id.first())
            oglas.save()
            for img in slike:
                photo = Slike.objects.create(slike = img, fk_oglas = oglas)
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


