
from re import template
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this

#from CarHub.forms import NewUserForm


# Create your views here.

def Test(request):
   # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStrana.html', {'imeSlike': 'carhublogo.png'})

def Ulogovan(request):
   # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStranaUlogovan.html')

def postavljanjeOglasa(request):
    return render(request, 'postavljanjeOglasa.html')

def prijava(request):
    return render(request,"prijavaProbaDjango.html")

def registracija(request):
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Registracija uspesna")
            return redirect("CarHub:pocetnaStranaUlogovan")
        messages.error(request,"Neuspesna registracija")
    form=NewUserForm()


    return render (request=request, template_name="registracijaProbaDjango.html", context={"register_form":form})
    #return render(request,"registracijaProbaDjango.html")


def prijava(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Ulogovani ste kao{username}.")
				return redirect("CarHub:pocetnaStranaUlogovan")
			else:
				messages.error(request,"Netacno ime ili lozinka.")
		else:
			messages.error(request,"Netacno ime ili lozinka.")
	form = AuthenticationForm()
	return render(request=request, template_name="prijavaProbaDjango.html", context={"login_form":form})

def logout(request):
    #logout(request)
    messages.info(request,"Uspesno ste izlogovani")
    return redirect("CarHub:pocetnaStrana")

