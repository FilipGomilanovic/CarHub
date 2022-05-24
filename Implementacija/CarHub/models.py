from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

# Ognjen Stanojevic 0585/2018


class Korisnik(AbstractUser):

    kontakt_telefon = models.CharField(db_column='Kontakt telefon', max_length=45)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slika = models.FileField(db_column='Slika',upload_to='imgs/' ,null=True,blank=True)  # Field name made lowercase.
    uloga = models.CharField(db_column='Uloga', max_length=1)  # Field name made lowercase.
    class Meta:
        db_table = 'korisnik'


class Model(models.Model):
    idmodel = models.AutoField(db_column='idModel', primary_key=True)  # Field name made lowercase.
    carreviewlink = models.CharField(db_column='CarReviewLink', max_length=500, blank=True, null=True)  # Field name made lowercase.
    brend = models.CharField(db_column='Brend', max_length=100)  # Field name made lowercase.
    naziv_modela = models.CharField(db_column='Naziv modela', max_length=100)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    godisteOd = models.IntegerField(db_column='GodisteOd', default=0)  #modeli su se pravili od nekog godista do drugog
    godisteDo = models.IntegerField(db_column='GodisteDo' , default=0)

    class Meta:
        db_table = 'model'


class Oglas(models.Model):
    idoglas = models.AutoField(db_column='idOglas', primary_key=True)  # Field name made lowercase.
    tip = models.CharField(db_column='Tip', max_length=1)  # Field name made lowercase.
    cena = models.IntegerField(db_column='Cena', blank=True, null=True)  # Field name made lowercase.
    boost = models.IntegerField(db_column='Boost', blank=True, null=True)  # Field name made lowercase.
    grad = models.CharField(db_column='Grad', max_length=45)  # Field name made lowercase.
    slike=models.FileField(db_column='Slike',upload_to='imgs/',null=True)
    snaga = models.IntegerField(db_column='Snaga', default=0)
    kilometraza = models.IntegerField(db_column='Kilometraza', default=0)
    godiste = models.IntegerField(db_column='Godiste', default=0)
    karoserija = models.CharField(db_column="Karoserija", max_length=20, null=False, blank=True, default="limuzina")
    model_idmodel = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='Model_idModel')  # Field name made lowercase.


    class Meta:
        db_table = 'oglas'

#
# class Cet(models.Model):
#     idcet = models.IntegerField(db_column='idCet', primary_key=True)  # Field name made lowercase.
#     korisnik_idkorisnika = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='Korisnik_idKorisnika')  # Field name made lowercase.
#     korisnik_idkorisnika1 = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='Korisnik_idKorisnika1')  # Field name made lowercase.
#     ip = models.CharField(max_length=30, blank=True, null=True)
#
#     class Meta:
#         db_table = 'cet'
#
#
# class Komentar(models.Model):
#     idkomentar = models.AutoField(db_column='idKomentar', primary_key=True)  # Field name made lowercase.
#     komentar = models.CharField(db_column='Komentar', max_length=500, blank=True, null=True)  # Field name made lowercase.
#     korisnik_idkorisnika_postavio = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='Korisnik_idKorisnika_Postavio')  # Field name made lowercase.
#     korisnik_idkorisnika1_naprofilu = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='Korisnik_idKorisnika1_NaProfilu')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'komentar'
#
#

#
#
# class Mojioglasi(models.Model):
#     idmojioglasi = models.IntegerField(db_column='idMojiOglasi', primary_key=True)  # Field name made lowercase.
#     korisnik_idkorisnika = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='Korisnik_idKorisnika')  # Field name made lowercase.
#     oglas_idoglas = models.ForeignKey('Oglas', models.DO_NOTHING, db_column='Oglas_idOglas')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'mojioglasi'
#         unique_together = (('idmojioglasi', 'korisnik_idkorisnika'),)
#
#
# class Ocena(models.Model):
#     idocena = models.IntegerField(db_column='idOcena', primary_key=True)  # Field name made lowercase.
#     ocena = models.IntegerField(db_column='Ocena', blank=True, null=True)  # Field name made lowercase.
#     korisnik_idkorisnika_postavio = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='Korisnik_idKorisnika_Postavio')  # Field name made lowercase.
#     korisnik_idkorisnika1_naprofilu = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='Korisnik_idKorisnika1_NaProfilu')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'ocena'
#
#

#
#
# class Poruke(models.Model):
#     idporuke = models.IntegerField(db_column='idPoruke', primary_key=True)  # Field name made lowercase.
#     poruka = models.CharField(db_column='Poruka', max_length=500, blank=True, null=True)  # Field name made lowercase.
#     cet_idcet = models.ForeignKey(Cet, models.DO_NOTHING, db_column='Cet_idCet')  # Field name made lowercase.
#     korisnik_idkorisnika = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='Korisnik_idKorisnika')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'poruke'
#
#
# class Sacuvanioglasi(models.Model):
#     idsacuvanioglasi = models.IntegerField(db_column='idSacuvaniOglasi', primary_key=True)  # Field name made lowercase.
#     korisnik_idkorisnika = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='Korisnik_idKorisnika')  # Field name made lowercase.
#     oglas_idoglas = models.ForeignKey(Oglas, models.DO_NOTHING, db_column='Oglas_idOglas')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'sacuvanioglasi'
#         unique_together = (('idsacuvanioglasi', 'korisnik_idkorisnika'),)
#
#
# class Termin(models.Model):
#     idtermin = models.AutoField(db_column='idTermin', primary_key=True)  # Field name made lowercase.
#     datumod = models.DateTimeField(db_column='DatumOd')  # Field name made lowercase.
#     datumdo = models.DateTimeField(db_column='DatumDo')  # Field name made lowercase.
#     korisnik_idkorisnika = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='Korisnik_idKorisnika')  # Field name made lowercase.
#     oglas_idoglas = models.ForeignKey(Oglas, models.DO_NOTHING, db_column='Oglas_idOglas')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'termin'
