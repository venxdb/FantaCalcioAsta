from django.contrib import admin
from django.core.management import call_command
from django import forms


from .models import Player_Quotes, PlayerQuotesFile, FullStatistics, Teams, Acquisti
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
@admin.register(Player_Quotes)
class PlayerQuotesAdmin(admin.ModelAdmin):

    list_display  = ("id", "ruolo", "ruolo_desc", "nome", "squadra", "quotazione_attuale", "quotazione_iniziale")
    search_fields = ("nome", "squadra", "ruolo_full")
    list_filter   = ("ruolo", "squadra") 

    actions       = ["update_player_quotes"]

    @admin.action(description="Aggiorna quotazioni giocatori")
    def update_player_quotes(self, request, queryset=None):
        call_command('update_player_quotes')
        self.message_user(request, "Quotazioni dei giocatori aggiornate con successo")

    update_player_quotes.short_description = "Aggiorna quotazioni giocatori"

    @admin.action(description="Test azione")
    def test_action(self, request, queryset):
        self.message_user(request, "Azione di test eseguita con successo")


@admin.register(PlayerQuotesFile)
class PlayerQuotesFileAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at")


@admin.register(FullStatistics)
class FullStatisticsAdmin(admin.ModelAdmin):

    list_display = ["id_player", "stagione", "club", "presenze","goal", "assist", "autogoal", "subentrato", "sostituito", 
                    "ammonizioni", "espulsioni_doppiogiallo", "espulsioni_dirette", "rigori_segnati", "minuti_pergoal",
                    "minuti_giocati"]
    
    actions      = ["update_statistics_ws"]

    @admin.action(description = "Aggiorna statistiche Transfermarkt dei giocatori")
    def update_statistics_ws(self, request, queryset = None):
        call_command("update_statistics_quotes")
        self.message_user("request", "Statistiche transfermarkt caricate. Visualizza log per vedere se alcune statistiche non sono state caricate")

    update_statistics_ws.short_description = "Aggiorna statistiche Transfermarkt"

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() if obj.first_name or obj.last_name else obj.username


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):

    list_display  = ["nome_squadra", "get_allenatore_full_name"]

    search_fields = ["nome_squadra", "allenatore__first_name", "allenatore__last_name"]

    def get_allenatore_full_name(self, obj):

        return f"{obj.allenatore.first_name} {obj.allenatore.last_name}".strip()
    
    get_allenatore_full_name.short_description = "FantaAllenatore"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "allenatore":
            # Usa la classe personalizzata per il campo di scelta
            return UserModelChoiceField(queryset=User.objects.all().order_by('first_name', 'last_name'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PlayerQuotesModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nome  # Mostra il nome del giocatore nel widget di selezione


@admin.register(Acquisti)
class AcquistiAdmin(admin.ModelAdmin):

    list_display        = ["get_allenatore_full_name", "get_giocatore_nome", "crediti"]

    autocomplete_fields = ["giocatore", "allenatore"]

    def get_allenatore_full_name(self, obj):

        return f"{obj.allenatore.first_name} {obj.allenatore.last_name}".strip()
    
    get_allenatore_full_name.short_description = "FantaAllenatore"

    def get_giocatore_nome(self, obj):

        return obj.giocatore.nome
    
    get_giocatore_nome.short_description = "Giocatore"



    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "allenatore":
            return UserModelChoiceField(queryset=User.objects.all().order_by('first_name', 'last_name'))
        
        if db_field.name == "giocatore":
            return PlayerQuotesModelChoiceField(queryset = Player_Quotes.objects.all().order_by('nome'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


