from django.core.management.base import BaseCommand
from astatracking.utils.player_quotes import get_cleaning_quotes, load_data_to_db
from astatracking.models import Player_Quotes

class Command(BaseCommand):

    help = "Aggiorna le quotazioni dei giocatori"

    def handle(self, *args, **options):

        df = get_cleaning_quotes()
        
        # dropping old quotes
        num_players = Player_Quotes.objects.count()
        Player_Quotes.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Cancellate vecchie quotazioni. N° istanze cancellate: {num_players}"))

        # loading
        self.stdout.write("Inizio caricamento quotazioni")
        load_data_to_db(df)
        num_players = Player_Quotes.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Numero di giocatori inseriti in tabella: {num_players}"))