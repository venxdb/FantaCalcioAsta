from django.db import models

# Create your models here.
class Player_Quotes(models.Model):

    id                  = models.IntegerField(primary_key = True)
    ruolo               = models.CharField(max_length = 1)
    ruolo_desc          = models.CharField(max_length = 20)
    nome                = models.CharField(max_length = 200)
    squadra             = models.CharField(max_length = 200)
    quotazione_attuale  = models.IntegerField()
    quotazione_iniziale = models.IntegerField()

