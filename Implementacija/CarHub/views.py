from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def Test(request):
   # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStrana.html', {'imeSlike': 'carhublogo.png'})




