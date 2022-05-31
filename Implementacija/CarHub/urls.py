from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name="CarHub"

urlpatterns = [

    path('pathTest', views.Test),
    path('postavljanjeOglasa', views.postavljanjeOglasa),
    path('profilKorisnika', views.profilKorisnika),

    path('pretragaOglasa', views.PretragaOglasa),
    path('pretragaOglasaRent', views.PretragaOglasaRent),

    path('urediProfil', views.urediProfil),


    path('pathTest', views.Test, name="pocetnaStrana"),
    path('pathTestUlogovan', views.Ulogovan, name="pocetnaStranaUlogovan"),


  # path('postavljanjeOglasa', views.postavljanjeOglasa),
    path('prijava',views.prijava),
    path('registracija',views.registracija),
    path('logout',views.logout,name="logout"),


    path('postavljanjeOglasa', views.postavljanjeOglasa),
    path('konkretanOglasProdaja/<int:oglas_id>',views.konkretanOglasProdaja),
    path('konkretanOglasRent/<int:oglas_id>',views.konkretanOglasRent)


]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)