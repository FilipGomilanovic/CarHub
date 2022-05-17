from django.urls import path
from . import views

app_name="CarHub"

urlpatterns = [
    path('pathTest', views.Test),
    path('postavljanjeOglasa', views.postavljanjeOglasa),

    path('pretragaOglasa', views.pretragaOglasa)


    path('pathTest', views.Test, name="pocetnaStrana"),
    path('pathTestUlogovan', views.Ulogovan, name="pocetnaStranaUlogovan"),

    path('postavljanjeOglasa', views.postavljanjeOglasa),
    path('prijava',views.prijava),
    path('registracija',views.registracija),
    path('logout',views.logout,name="logout")

]