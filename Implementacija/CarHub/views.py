
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import *
from json import dumps
from django.http import HttpResponseRedirect


# from CarHub.forms import NewUserForm


# Create your views here.


def Test(request):
    # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStrana.html', {'imeSlike': 'carhublogo.png'})


def Ulogovan(request):
    # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStranaUlogovan.html')


@login_required(login_url='login')
def profilKorisnika(request):
    trenutni = request.user
    komentar = Komentar.objects.order_by('-timestamp').filter(profilKorisnika=trenutni)
    oceneKorisnika = Ocena.objects.all().filter(korisnik=trenutni)
    ukupnoOcena = Ocena.objects.all().filter(korisnik=trenutni).count()
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
        'data': data

    }
    return render(request, 'profilKorisnika.html', context)


def profilDrugogKorisnika(request, korisnik_id):
    profil = Korisnik.objects.get(id=korisnik_id)
    komentar = Komentar.objects.order_by('-timestamp').filter(profilKorisnika=profil)
    oceneKorisnika = Ocena.objects.all().filter(korisnik=profil)

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
        'ocenaUlogovanog': ocenaUlogovanog
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


def urediProfil(request):
    # try:
    #     profil = Korisnik
    #
    #     context = {    #     }
    return render(request, 'urediProfil.html')


# except Korisnik.DoesNotExist:
#     raise Http404("Korisnik not found")


def postavljanjeOglasa(request):
    forma = PostavljanjeOglasa(request.POST, request.FILES)
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
        "brendovi": brendovi,
        "forma_postaviOglas": forma
    }
    return render(request=request, template_name='testForme.html', context=context)


def registracija(request):
    form = KorisnikNoviForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("CarHub:pocetnaStranaUlogovan")

    form = KorisnikNoviForm()
    return render(request=request, template_name="registracijaProbaDjango.html", context={"register_form": form})
    # return render(request,"registracijaProbaDjango.html")


def pretragaOglasa(request):
    return render(request, 'pretragaOglasa.html')


def pregledOglasa(request):
    return render(request, 'pregledOglasa.html')


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
