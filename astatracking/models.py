from django.db import models
import os
from django.contrib.auth.models import User

# Create your models here.

"""
    Modello quotazioni
"""
class Player_Quotes(models.Model):

    id                  = models.IntegerField(primary_key = True)
    ruolo               = models.CharField(max_length = 1)
    ruolo_desc          = models.CharField(max_length = 20)
    nome                = models.CharField(max_length = 200)
    squadra             = models.CharField(max_length = 200)
    quotazione_attuale  = models.IntegerField()
    quotazione_iniziale = models.IntegerField()


"""
    Modello per il caricamento del file delle quotazioni
"""

class PlayerQuotesFile(models.Model):

    file        = models.FileField(upload_to='static/player_quotes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} loaded successfully"
    
    def save(self, *args, **kwargs):

        if PlayerQuotesFile.objects.exists():
            old_file = PlayerQuotesFile.objects.latest('uploaded_at')
            if old_file.file and os.path.isfile(old_file.file.path):
                os.remove(old_file.file.path)
            
            old_file.delete()
        
        super().save(*args, **kwargs)


"""
    Modello per statistiche transfermarkt
"""

class FullStatistics(models.Model):

    id_player               = models.ForeignKey(Player_Quotes, on_delete=models.CASCADE, related_name='statistics')
    stagione                = models.CharField(max_length = 250)
    club                    = models.CharField(max_length = 250)
    presenze                = models.IntegerField()
    goal                    = models.IntegerField()
    assist                  = models.IntegerField()
    autogoal                = models.IntegerField()
    subentrato              = models.IntegerField()
    sostituito              = models.IntegerField()
    ammonizioni             = models.IntegerField()
    espulsioni_doppiogiallo = models.IntegerField()
    espulsioni_dirette      = models.IntegerField()
    rigori_segnati          = models.IntegerField()
    minuti_pergoal          = models.IntegerField()
    minuti_giocati          = models.IntegerField()
    goal_subiti             = models.IntegerField(default = 0)
    clean_sheets            = models.IntegerField(default = 0)


"""
    Modello per le squadre dei partecipanti
"""

class Teams(models.Model):

    id            = models.AutoField(primary_key = True)
    allenatore    = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "teams")
    nome_squadra  = models.CharField(max_length = 250)
    
    def __str__(self):
        return f"{self.nome_squadra} (Allenatore: {self.allenatore.username})"
    
    class Meta:
        verbose_name        = "Team"
        verbose_name_plural = "Teams"


"""
    Modello per gli acquisti
"""

class Acquisti(models.Model):

    id         = models.AutoField(primary_key = True)
    allenatore = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "acquisti")
    giocatore  = models.ForeignKey(Player_Quotes, on_delete = models.CASCADE, related_name = "acquisti")
    crediti    = models.IntegerField()

    def __str__(self):
        return f"{self.giocatore.nome} - {self.allenatore.username} - {self.crediti}"
    
    @classmethod
    def crea_acquisti_pertutti_utenti(cls):

        ruoli = {
                    "Portiere": 3, 
                    "Difensore": 8,
                    "Centrocampista": 8,
                    "Attaccante": 6
                }

        utenti = User.objects.all()

        for utente in utenti:
            if utente != "admin":
                print(f"Inserimento acquisti per {utente.username}")

                for ruolo, num_giocatori in ruoli.items():
                    giocatori = Player_Quotes.objects.filter(ruolo_desc = ruolo)

                    giocator_scelti = random.sample(list(giocatori),num_giocatori)
                    print(f"Giocatori scelti: {giocator_scelti}")

                    for g in giocator_scelti:
                        cls.objects.create(
                            allenatore = utente, 
                            giocatore = g,
                            crediti = 10
                        )
                print(f"Acquisti completati per {utente.username}")