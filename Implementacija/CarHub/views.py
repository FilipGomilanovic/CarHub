from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from django.template.defaultfilters import register

from .forms import *
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from json import dumps
import datetime
from datetime import datetime
from django.http import HttpResponseRedirect
from django.db.models import Q


# Create your views here.

@register.filter
def index(sequence, position):
    return sequence[position]


def pocetnaStrana(request):
    return render(request, 'pocetnaStrana.html', {'imeSlike': 'carhublogo.png'})


def Ulogovan(request):
    return render(request, 'pocetnaStrana.html')


def BoostOglasa(request, oglas_id):
    if request.method == 'POST':
        oglas = Oglas.objects.get(idoglas=oglas_id)
        oglas.boost = 1;
        oglas.save();
        if oglas.tip == 'p':
            return HttpResponseRedirect("/konkretanOglasProdaja/" + str(oglas_id))
        else:
            return HttpResponseRedirect("/konkretanOglasRent/" + str(oglas_id))

    context = {

        'id': oglas_id
    }
    return render(request, 'boostOglasa.html', context)


@login_required(login_url='prijava.html')
def profilKorisnika(request):
    trenutni = request.user
    komentar = Komentar.objects.order_by('-timestamp').filter(profilKorisnika=trenutni)
    oceneKorisnika = Ocena.objects.all().filter(korisnik=trenutni)
    ukupnoOcena = Ocena.objects.all().filter(korisnik=trenutni).count()

    mojiOglasi = MojiOglasi.objects.values_list('oglas_id', flat=True).filter(korisnik_id=trenutni)
    sacuvaniOglasi = SacuvaniOglasi.objects.values_list('oglas_id', flat=True).filter(korisnik_id=trenutni)
    nizMojihOglasa = []
    nizSacuvanihOglasa = []
    imgs = []
    imgs2 = []
    brendovi = []
    brendovi2 = []
    modeli = []
    modeli2 = []
    nizBrendova = []
    nizBrendova2 = []
    tipovi = []
    tipovi2 = []

    for oglas in mojiOglasi:
        o = Oglas.objects.get(idoglas=oglas)

        nizMojihOglasa.append(o);
        nesto = Slike.objects.filter(fk_oglas=oglas)
        imgs.append(nesto.first().slike)
        tipovi.append(o.tip)

        m = Model.objects.get(idmodel=o.model_idmodel.idmodel)
        nizBrendova.append(m)
    for i in nizBrendova:
        brendovi.append(i.brend)
        modeli.append(i.naziv_modela)
    # //////////////////////////////////////////////////
    for oglas in sacuvaniOglasi:
        o = Oglas.objects.get(idoglas=oglas)

        nizSacuvanihOglasa.append(o);
        nesto = Slike.objects.filter(fk_oglas=oglas)
        imgs2.append(nesto.first().slike)
        tipovi2.append(o.tip)

        m = Model.objects.get(idmodel=o.model_idmodel.idmodel)
        nizBrendova2.append(m)
    for i in nizBrendova2:
        brendovi2.append(i.brend)
        modeli2.append(i.naziv_modela)

    ocene1 = 0
    ocene2 = 0
    ocene3 = 0
    ocene4 = 0
    ocene5 = 0

    for o in oceneKorisnika:
        if o.ocena == 1:
            ocene1 = ocene1 + 1
        elif o.ocena == 2:
            ocene2 = ocene2 + 1
        elif o.ocena == 3:
            ocene3 = ocene3 + 1
        elif o.ocena == 4:
            ocene4 = ocene4 + 1
        elif o.ocena == 5:
            ocene5 = ocene5 + 1

    if ukupnoOcena != 0:
        ocene1Bar = ocene1 / ukupnoOcena * 100
        ocene2Bar = ocene2 / ukupnoOcena * 100
        ocene3Bar = ocene3 / ukupnoOcena * 100
        ocene4Bar = ocene4 / ukupnoOcena * 100
        ocene5Bar = ocene5 / ukupnoOcena * 100
    else:
        ocene1Bar = 0
        ocene2Bar = 0
        ocene3Bar = 0
        ocene4Bar = 0
        ocene5Bar = 0
    if ukupnoOcena > 0:
        prosecnaOcena = (ocene1 + ocene2 * 2 + ocene3 * 3 + ocene4 * 4 + ocene5 * 5) / ukupnoOcena
        prosecnaOcena = (round(prosecnaOcena, 2))
        if prosecnaOcena > 2.5:
            if prosecnaOcena < 3.5:
                zvezdice = 3
            elif prosecnaOcena > 4.5:
                zvezdice = 5
            else:
                zvezdice = 4
        else:
            if prosecnaOcena > 1.5:
                zvezdice = 2
            elif prosecnaOcena < 0.5:
                zvezdice = 1
            else:
                zvezdice = 0

    else:
        prosecnaOcena = 0
        zvezdice = 0

    data = []
    for i in range(5):
        data.append(i + 1)

    context = {
        'komentar': komentar,
        'ocene1': ocene1,
        'ocene2': ocene2,
        'ocene3': ocene3,
        'ocene4': ocene4,
        'ocene5': ocene5,
        'ukupnoOcena': ukupnoOcena,
        'prosecnaOcena': prosecnaOcena,
        'ocene1Bar': ocene1Bar,
        'ocene2Bar': ocene2Bar,
        'ocene3Bar': ocene3Bar,
        'ocene4Bar': ocene4Bar,
        'ocene5Bar': ocene5Bar,
        'zvezdice': zvezdice,
        'data': data,
        'nizMojihOglasa': nizMojihOglasa,
        'nizSacuvanihOglasa': nizSacuvanihOglasa,
        'slike': imgs,
        'brendovi': brendovi,
        'modeli': modeli,
        'tipovi': tipovi,
        'slike2': imgs2,
        'brendovi2': brendovi2,
        'modeli2': modeli2,
        'tipovi2': tipovi2

    }
    return render(request, 'profilKorisnika.html', context)


def profilDrugogKorisnika(request, korisnik_id):
    profil = Korisnik.objects.get(id=korisnik_id)
    komentar = Komentar.objects.order_by('-timestamp').filter(profilKorisnika=profil)
    oceneKorisnika = Ocena.objects.all().filter(korisnik=profil)

    mojiOglasi = MojiOglasi.objects.values_list('oglas_id', flat=True).filter(korisnik_id=korisnik_id)
    nizMojihOglasa = []
    imgs = []
    brendovi = []
    modeli = []
    nizBrendova = []
    for oglas in mojiOglasi:
        o = Oglas.objects.get(idoglas=oglas)
        nizMojihOglasa.append(o);
        nesto = Slike.objects.filter(fk_oglas=oglas)
        imgs.append(nesto.first().slike)

        m = Model.objects.get(idmodel=o.model_idmodel.idmodel)
        nizBrendova.append(m)
    for i in nizBrendova:
        brendovi.append(i.brend)
        modeli.append(i.naziv_modela)

    tempOcena = Ocena.objects.filter(ocenio=request.user, korisnik=profil)

    if oceneKorisnika.filter(ocenio=request.user):
        ocenjen = 1
        ocenaUlogovanog = tempOcena.first().ocena

    else:
        ocenjen = 0
        ocenaUlogovanog = -1

    ukupnoOcena = Ocena.objects.all().filter(korisnik=profil).count()

    if request.method == 'POST':
        form = KomentarForm(request.POST or None)
        if form.is_valid():
            kom = form.save(commit=False)
            kom.autor = request.user
            kom.profilKorisnika = profil
            kom.save()
            return HttpResponseRedirect(request.path_info)
    form = KomentarForm()
    kom_id = request.POST.get('komentar_id')
    if kom_id:
        kom = Komentar.objects.get(pk=kom_id)
        kom.delete()
        return HttpResponseRedirect(request.path_info)
    user_id = request.POST.get('profil_id')
    if user_id:
        user = Korisnik.objects.get(pk=user_id)
        user.delete()
        return HttpResponseRedirect('/pocetnaStrana')

    if request.method == "POST":
        rate = request.POST.get('rate')
        if rate is None:
            pass
        else:
            if str(rate) == '1':
                ocena = Ocena(ocena=5, korisnik=profil, ocenio=request.user)
                ocena.save()  # Naopaki su brojevi jer su radioButtoni naopaki
            elif str(rate) == '2':
                ocena = Ocena(ocena=4, korisnik=profil, ocenio=request.user)
                ocena.save()
            elif str(rate) == '3':
                ocena = Ocena(ocena=3, korisnik=profil, ocenio=request.user)
                ocena.save()
            elif str(rate) == '4':
                ocena = Ocena(ocena=2, korisnik=profil, ocenio=request.user)
                ocena.save()
            elif str(rate) == '5':
                ocena = Ocena(ocena=1, korisnik=profil, ocenio=request.user)
                ocena.save()
            else:
                print("greska")
        return HttpResponseRedirect(request.path_info)

    ocene1 = 0
    ocene2 = 0
    ocene3 = 0
    ocene4 = 0
    ocene5 = 0

    for o in oceneKorisnika:
        if o.ocena == 1:
            ocene1 = ocene1 + 1
        elif o.ocena == 2:
            ocene2 = ocene2 + 1
        elif o.ocena == 3:
            ocene3 = ocene3 + 1
        elif o.ocena == 4:
            ocene4 = ocene4 + 1
        elif o.ocena == 5:
            ocene5 = ocene5 + 1

    if ukupnoOcena != 0:
        ocene1Bar = ocene1 / ukupnoOcena * 100
        ocene2Bar = ocene2 / ukupnoOcena * 100
        ocene3Bar = ocene3 / ukupnoOcena * 100
        ocene4Bar = ocene4 / ukupnoOcena * 100
        ocene5Bar = ocene5 / ukupnoOcena * 100
    else:
        ocene1Bar = 0
        ocene2Bar = 0
        ocene3Bar = 0
        ocene4Bar = 0
        ocene5Bar = 0

    if ukupnoOcena > 0:
        prosecnaOcena = (ocene1 + ocene2 * 2 + ocene3 * 3 + ocene4 * 4 + ocene5 * 5) / ukupnoOcena
        prosecnaOcena = (round(prosecnaOcena, 2))
        if prosecnaOcena > 2.5:
            if prosecnaOcena < 3.5:
                zvezdice = 3
            elif prosecnaOcena > 4.5:
                zvezdice = 5
            else:
                zvezdice = 4
        else:
            if prosecnaOcena > 1.5:
                zvezdice = 2
            elif prosecnaOcena < 0.5:
                zvezdice = 1
            else:
                zvezdice = 0
    else:
        prosecnaOcena = 0

    if prosecnaOcena > 2.5:
        if prosecnaOcena < 3.5:
            zvezdice = 3
        elif prosecnaOcena > 4.5:
            zvezdice = 5
        else:
            zvezdice = 4
    else:
        if prosecnaOcena > 1.5:
            zvezdice = 2
        elif prosecnaOcena < 0.5:
            zvezdice = 1
        else:
            zvezdice = 0

    data = []
    for i in range(5):
        data.append(i + 1)

    context = {
        'profil': profil,
        'komentar': komentar,
        'ocene1': ocene1,
        'ocene2': ocene2,
        'ocene3': ocene3,
        'ocene4': ocene4,
        'ocene5': ocene5,
        'ukupnoOcena': ukupnoOcena,
        'prosecnaOcena': prosecnaOcena,
        'ocene1Bar': ocene1Bar,
        'ocene2Bar': ocene2Bar,
        'ocene3Bar': ocene3Bar,
        'ocene4Bar': ocene4Bar,
        'ocene5Bar': ocene5Bar,
        'zvezdice': zvezdice,
        'data': data,
        'form': form,
        'ocenjen': ocenjen,
        'ocenaUlogovanog': ocenaUlogovanog,
        'nizMojihOglasa': nizMojihOglasa,
        'slike': imgs,
        'brendovi': brendovi,
        'modeli': modeli

    }
    return render(request, 'profilDrugogKorisnika.html', context)


@login_required(login_url='login')
def create_Komentar(request):
    form = KomentarForm(request.POST or None)
    if form.is_valid():
        kom = form.save(commit=False)
        kom.autor = Korisnik.objects.get(username=request.user.get_username())
        kom.save()
        return redirect('profilDrugogKorisnika.html')


def konkretanOglasProdaja(request, oglas_id):
    try:
        vecSacuvan = SacuvaniOglasi.objects.get(korisnik_id=request.user, oglas_id=oglas_id)
        vecSacuvan = 1
    except SacuvaniOglasi.DoesNotExist:
        vecSacuvan = 0

    oglas = Oglas.objects.get(pk=oglas_id)
    model_oglasa = oglas.model_idmodel
    lista_slika = list(Slike.objects.filter(fk_oglas=oglas))
    korisnik = MojiOglasi.objects.get(oglas_id=oglas_id).korisnik_id
    variable = request.POST.get("sacuvaj")
    if variable:
        o = Oglas.objects.get(pk=variable)
        sacuvaniOglasi = SacuvaniOglasi(korisnik_id=request.user, oglas_id=o)
        sacuvaniOglasi.save();
        return HttpResponseRedirect(request.path_info)

    brisi = request.POST.get('oglas_id')
    if brisi:
        tren_oglas = Oglas.objects.get(pk=brisi)
        tren_oglas.delete()
        return HttpResponseRedirect('/profilKorisnika')
    print(korisnik)

    print(lista_slika[0].slike)
    oglas_dict = {
        'brend': model_oglasa.brend,
        'link': model_oglasa.carreviewlink,
        'model': model_oglasa.naziv_modela,
        'cena': oglas.cena,
        'boost': oglas.boost,
        'slike': lista_slika,
        'snaga': oglas.snaga,
        'kilometraza': oglas.kilometraza,
        'godiste': oglas.godiste,
        'karoserija': oglas.karoserija,
        'opis': oglas.opis,
        'ime': korisnik.username,
        'mail': korisnik.email,
        'broj': korisnik.kontakt_telefon,
        'id': oglas_id,
        'vlasnik': oglas.vlasnik_id,
        'vecSacuvan': vecSacuvan
    }

    return render(request, 'konkretanOglasProdaja.html', context={'oglas': oglas_dict})


def konkretanOglasRent(request, oglas_id):
    poruka = ""
    datumi = []
    korisnik = MojiOglasi.objects.get(oglas_id=oglas_id).korisnik_id
    variable = request.POST.get("sacuvaj")
    if variable:
        o = Oglas.objects.get(pk=variable)
        sacuvaniOglasi = SacuvaniOglasi(korisnik_id=request.user, oglas_id=o)
        sacuvaniOglasi.save();
        return HttpResponseRedirect(request.path_info)

    brisi = request.POST.get('oglas_id')
    if brisi:
        tren_oglas = Oglas.objects.get(pk=brisi)
        tren_oglas.delete()
        return HttpResponseRedirect('/profilKorisnika')

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

    # print(datumPocetni)
    oglas_dict = {
        'brend': model_oglasa.brend,
        'model': model_oglasa.naziv_modela,
        'cena': oglas.cena,
        'grad': oglas.grad,
        'boost': oglas.boost,
        'slike': lista_slika,
        'karoserija': oglas.karoserija,
        'godiste': oglas.godiste,
        'datumDanasnji': datumPocetni,
        'poruka': poruka,
        'ime': korisnik.username,
        'mail': korisnik.email,
        'broj': korisnik.kontakt_telefon,
        'id': oglas_id,
        'vlasnik': oglas.vlasnik_id
    }

    return render(request, 'konkretanOglasRent.html', context=oglas_dict)


def urediProfil(request):
    trenutniKorisnik = request.user
    kime = None
    pas = None
    fon = None
    mail = None
    tren = request.POST.get('profil_id')
    if tren:
        korisnik = Korisnik.objects.get(pk=tren)
        korisnik.delete()
        return HttpResponseRedirect('/registracija')
    form = PromeniSliku(request.POST or None, request.FILES or None)
    if form.is_valid():
        kime = request.POST['ime1']
        pas = request.POST['sifra1']
        fon = request.POST.get('telefon1')
        mail = request.POST.get('mejl1')
        slika = form.cleaned_data.get('slika')
        if slika is not None:
            trenutniKorisnik.slika = slika

        if len(kime) > 6:
            trenutniKorisnik.username = kime
        if len(pas) > 6:
            trenutniKorisnik.set_password(pas)
        if len(fon) > 6:
            trenutniKorisnik.kontakt_telefon = fon
        if len(mail) > 6:
            trenutniKorisnik.email = mail
        trenutniKorisnik.save()
    context = {
        "forma_promenaSlike": form
    }

    return render(request, 'urediProfil.html', context=context)


def PretragaOglasa(request):
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela").distinct())
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    poruka = ""
    forma = pretragaOglasa(request.POST or None)
    if forma.is_valid():
        brend = request.POST['dropdown_Brend']
        naziv_model = request.POST['dropdown_Model']
        godiste1 = forma.cleaned_data.get('godiste1')
        godiste2 = forma.cleaned_data.get('godiste2')
        karoserija = forma.cleaned_data.get('karoserija')
        cenaOd = forma.cleaned_data.get('cena1')
        cenaDo = forma.cleaned_data.get('cena2')
        if cenaDo is None:
            cenaDo = 10000000000
        if cenaOd is None:
            cenaOd = 0
        if godiste1 is None:
            godiste1 = 0
        if godiste2 is None:
            godiste2 = 10000000000
        # print(brend)
        # print(naziv_model)
        oglasi = []
        oglasi_pom = []
        imgs = []
        oglasi_pom.extend(list(Oglas.objects.filter(godiste__lte=godiste2).filter(
            godiste__gte=godiste1).filter(karoserija=karoserija).filter(cena__gte=cenaOd).filter(
            cena__lte=cenaDo).filter(tip="p")))

        for oglas in oglasi_pom:
            idMod = oglas.model_idmodel
            if (idMod.brend == brend and idMod.naziv_modela == naziv_model):
                oglasi.append(oglas)

        if len(oglasi) != 0:
            for oglas in oglasi:
                nesto = Slike.objects.filter(fk_oglas=oglas)
                imgs.append(nesto.first().slike)
                # imgs.append((Slike.objects.filter(fk_oglas=oglas)).first().slike)
                print(imgs)
        else:
            poruka = "Nema oglasa!"

        dataJSON = dumps(niz)
        context = {
            "naziv_brenda": brend,
            "naziv_modela": naziv_model,
            "slike": imgs,
            "oglasi": oglasi,
            "data": dataJSON,
            "brendovi": brendovi,  # sluzi za padajucu listu
            "forma_pretraziOglas": forma,
            "poruka": poruka
        }

        return render(request=request, template_name='pretragaOglasa.html', context=context)

    # ako je korisnik poslat na stranicu pretrage preko get requesta, to znaci da je to prvi ulaz tu,
    # a ako je preko post requesta, onda je vec napravio filtere i primenio ih
    # U slucaju da korisnik dolazi na sajt get requestom, pravi se lista od pocetnih 9 oglasa(boostovani, ili svi boos
    # tovani sa skrolom), a u slucaju da se dolazi na sajt nakon post requesta, onda se primenjuju filteri i
    # salju odgovarajuci oglasi

    # ovde ide kod za dobijanje boostovanih oglasa i njihovo slanje nakon GET request-a
    oglasi = []
    imgs = []

    brend_model = []  # lista naziva brenda i modela koju saljem kroz kontekst u slucaju da je get metod
    oglasi.extend(list(Oglas.objects.filter(boost=1).filter(tip='p')))

    print("pretraga oglasa - GET")

    if len(oglasi) != 0:
        for oglas in oglasi:
            model = Model.objects.get(idmodel=oglas.model_idmodel.idmodel)
            brend_model.append(str(model.brend) + " " + str(model.naziv_modela))
            nesto = Slike.objects.filter(fk_oglas=oglas)
            imgs.append(nesto.first().slike)
    else:
        poruka = "Nema oglasa!"

    # ovde ide kod za dobijanje boostovanih oglasa i njihovo slanje nakon GET request-a

    dataJSON = dumps(niz)
    context = {
        "naziv_brenda_modela_list": brend_model,
        "slike": imgs,
        "oglasi": oglasi,
        "data": dataJSON,
        "brendovi": brendovi,  # za padajucu listu
        "forma_pretraziOglas": forma,
        "poruka": poruka
    }
    return render(request=request, template_name='pretragaOglasa.html', context=context)


def PretragaOglasaRent(request):
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela").distinct())
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
        oglasi_pom2 = []
        oglasi_pom2 = list(Oglas.objects.filter(grad=grad).filter(tip="r"))
        for ogl in oglasi_pom2:
            if ogl.model_idmodel.brend == brend and ogl.model_idmodel.naziv_modela:
                oglasi_pom.append(ogl)

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
                        if (not (datumOd.strftime("%d-%m-%y") > datum.datumDo.strftime("%d-%m-%y") or datumDo.strftime(
                                "%d-%m-%y") < datum.datumOd.strftime("%d-%m-%y"))):
                            fleg = False;
                    if fleg == True:
                        oglasi.append(oglas)

                for oglas in oglasi:
                    nesto = Slike.objects.filter(fk_oglas=oglas)
                    imgs.append(nesto.first().slike)
                    # imgs.append((Slike.objects.filter(fk_oglas=oglas)).first().slike)
                    #print(imgs)
            else:
                oglasi = oglasi_pom
                for oglas in oglasi:
                    nesto = Slike.objects.filter(fk_oglas=oglas)
                    imgs.append(nesto.first().slike)
                #print(oglasi)
        else:
            poruka = "Nema oglasa!"
        dataJSON = dumps(niz)
        context = {
            "naziv_brenda": brend,
            "naziv_modela": naziv_model,
            "oglasi": oglasi,
            "data": dataJSON,
            "brendovi": brendovi,
            "forma_pretraziOglasRent": form,
            "slike": imgs,
            "poruka": poruka
        }
        #print(oglasi)
        return render(request=request, template_name='pretragaOglasaRent.html', context=context)

    oglasi = []
    imgs = []
    brend_model = []  # lista naziva brenda i modela koju saljem kroz kontekst u slucaju da je get metod
    oglasi.extend(list(Oglas.objects.filter(tip='r').filter(boost=1)))
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
        "brendovi": brendovi,
        "forma_pretraziOglasRent": form,
        "poruka": poruka
    }
    return render(request=request, template_name='pretragaOglasaRent.html', context=context)


@login_required(login_url='login')
def postavljanjeOglasa(request):
    form = PostavljanjeOglasa(request.POST or None, request.FILES or None)
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
            brend=brend).filter(naziv_modela=naziv_model)  # filtriranje radi pronalaska id-ja modela

        # print(model_id)
        # proveriti sta vraca post request za izbor (da li vraca value od pritisnitog dugmeta)
        if (izbor == "prodaja"):
            cena = request.POST["cenaProdaja"];
            for img in slike:
                print(img)
            oglas = Oglas(tip="p", cena=cena, boost=0, grad='', slike=slike,
                          snaga=snaga, kilometraza=kilometraza, karoserija=karoserija,
                          godiste=godiste, model_idmodel=model_id.first())
            id = oglas.idoglas
            oglas.vlasnik_id = request.user
            oglas.save()
            for img in slike:
                photo = Slike.objects.create(slike=img, fk_oglas=oglas)
            mojOglas = MojiOglasi(korisnik_id=request.user, oglas_id=oglas)
            mojOglas.save()

        else:
            cena = request.POST["cenaIznajmljivanje"];
            grad = request.POST["Grad"]
            oglas = Oglas(tip="r", cena=cena, boost=0, grad=grad, slike=slike,
                          snaga=snaga, kilometraza=kilometraza, karoserija=karoserija,
                          godiste=godiste, model_idmodel=model_id.first())

            oglas.vlasnik_id = request.user
            oglas.save()

            for img in slike:
                photo = Slike.objects.create(slike=img, fk_oglas=oglas)

            mojOglas = MojiOglasi(korisnik_id=request.user, oglas_id=oglas)
            mojOglas.save()

        # napraviti razlicite ifove za prodaju i iznajmljivanje
        # ako je prodaja, moze odmag da se postavi oglas
        # ako je iznajmljivanje, treba smisliti nacin za kupljenje datuma i za njihovubacivanje u bazu
        # takodje, mora se naci id_Modela pomocu brenda, modela i godista

    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela").distinct())
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    # print(niz)
    # print(brendovi_modeli)

    dataJSON = dumps(niz)
    context = {
        "data": dataJSON,
        "brendovi": brendovi,
        "forma_postaviOglas": form
    }
    return render(request=request, template_name='postavljanjeOglasa.html', context=context)


def registracija(request):
    form = KorisnikNoviForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("CarHub:pocetnaStrana")

    form = KorisnikNoviForm()
    return render(request=request, template_name="registracija.html", context={"register_form": form})
    # return render(request,"registracijaProbaDjango.html")


def prijava(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)  # moraju da se taguju
            if user is not None:
                login(request, user)
                messages.info(request, f"Ulogovani ste kao{username}.")
                return redirect("CarHub:pocetnaStrana")
            else:
                messages.error(request, "Netacno ime ili lozinka.")
        else:
            messages.error(request, "Netacno ime ili lozinka.")
    form = AuthenticationForm()
    return render(request=request, template_name="prijava.html", context={"login_form": form})


def logout(request):
    print("Usao")
    auth.logout(request)
    return redirect("CarHub:pocetnaStrana")


def cet(request, idKor):
    try:
        CetKorisnik = Korisnik.objects.get(id=idKor)
    except Korisnik.DoesNotExist:
        CetKorisnik = None

    trenutni = request.user
    try:
        trenutniCet = Cet.objects.get(idkorisnika1=trenutni, idkorisnika2=idKor)
    except Cet.DoesNotExist:
        trenutniCet = None

    if trenutniCet is None:
        try:
            trenutniCet = Cet.objects.get(idkorisnika2=trenutni, idkorisnika1=idKor)
        except Cet.DoesNotExist:
            trenutniCet = None
    if trenutniCet is not None:
        if trenutniCet.idkorisnika1 == trenutni:
            trenutniCet.ne_procitano_Korisnik_1 = 'N'
            trenutniCet.save()
        else:
            trenutniCet.ne_procitano_Korisnik_2 = 'N'
            trenutniCet.save()

    sviKorisnici = []
    cetovi = Cet.objects.order_by('-timestamp').filter(Q(idkorisnika1=trenutni) | Q(idkorisnika2=trenutni))
    searchform = CetSearchForm(data=request.POST or None)
    if searchform.is_valid():
        print("search")
        term = searchform.cleaned_data.get('term')
        for i in cetovi:
            if i.idkorisnika1 == trenutni:
                if term in i.idkorisnika2.username:
                    sviKorisnici.append([i.idkorisnika2, i.ne_procitano_Korisnik_1])
            else:
                if term in i.idkorisnika1.username:
                    sviKorisnici.append([i.idkorisnika1, i.ne_procitano_Korisnik_2])
    else:
        print("nijeSearch")
        for i in cetovi:
            if i.idkorisnika1 == trenutni:
                sviKorisnici.append([i.idkorisnika2, i.ne_procitano_Korisnik_1])
            else:
                sviKorisnici.append([i.idkorisnika1, i.ne_procitano_Korisnik_2])

    if trenutniCet is None:
        svePoruke = []
    else:
        svePoruke = Poruke.objects.all().filter(cet_idcet=trenutniCet)

    send = request.POST.get('send')
    if send:
        print("usao")
        form = PorukaForm(request.POST or None)
        if form.is_valid():
            por = form.save(commit=False)
            por.idKorisnikaPoslao = trenutni
            if trenutniCet is None:
                noviCet = Cet(idkorisnika1=trenutni, idkorisnika2=CetKorisnik, ne_procitano_Korisnik_1='N',
                              ne_procitano_Korisnik_2='Y')
                noviCet.save()
                por.cet_idcet = noviCet
                por.timestamp = datetime.now()
                por.save()
            else:
                trenutniCet.timestamp = datetime.now()
                por.cet_idcet = trenutniCet
                por.timestamp = datetime.now()
                por.save()
                if trenutniCet.idkorisnika1 == trenutni:
                    trenutniCet.ne_procitano_Korisnik_2 = 'Y'
                    trenutniCet.save()
                else:
                    trenutniCet.ne_procitano_Korisnik_1 = 'Y'
                    trenutniCet.save()

            return HttpResponseRedirect(request.path_info)

    form = PorukaForm()

    context = {
        'sviKorisnici': sviKorisnici,
        'svePoruke': svePoruke,
        'formaPoruke': form,
        'idKor': CetKorisnik,
        'id': idKor,
        'searchform': searchform
    }
    # Popraviti
    if idKor == 0:
        context['formaPoruke'] = 'Nema'

    return render(request, 'cet.html', context)
