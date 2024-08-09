from django.contrib import admin
from .models import Player_Quotes

# Register your models here.
@admin.register(Player_Quotes)
class PlayerQuotesAdming(admin.ModelAdmin):

    list_display  = ("id", "ruolo", "ruolo_desc", "nome", "squadra", "quotazione_attuale", "quotazione_iniziale")
    search_fields = ("nome", "squadra", "ruolo_full")
    list_filter   = ("ruolo", "squadra") 