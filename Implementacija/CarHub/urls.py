from django.urls import path
from . import views

urlpatterns = [
    path('pathTest', views.Test),
    path('postavljanjeOglasa', views.postavljanjeOglasa),
    path('pretragaOglasa', views.pretragaOglasa)
]