from django.contrib import admin
from django.core.management import call_command

from .models import Player_Quotes, PlayerQuotesFile


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