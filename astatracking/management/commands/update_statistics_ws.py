from django.core.management.base import BaseCommand
from astatracking.utils.player_statistics_ws import get_statistics_player, cleaning_transfermarkt_data
from astatracking.models import Player_Quotes, FullStatistics
import pandas as pd


class Command(BaseCommand):

    help = "Aggiorna le statistiche da transfermarkt"

    def handle(self, *args, **options):

        # get tutti i giocatori presenti nella tabella quotazioni
        players           = Player_Quotes.objects.all()
        player_dict       = {player.id: player for player in players}

        # lista player statistiche non caricate
        player_nostats    = []
        competizioni      = ["Serie A", "Serie B", "Premier League", "Ligue 1", "Bundesliga", "LaLiga", "Eredivisie"]

        # web scraping for statistics
        for player_id, player_instance in player_dict.items():
            player_name = player_instance.nome
            
            column_names = ["Stagione", "Competizione", "Club", "Convocazioni", "Presenze", "Goals",
                    "Assists", "Autogoal",
                    "Subentrato", "Sostituito", "Ammonito", "Espulso Doppio Giallo", "Espulsione diretta",
                    "Goal su rigore",
                    "Minuti per Goal", "Minuti Giocati", "Goal subiti", "Clean Sheets"]
            
            try: 
                df_statistics = get_statistics_player(player_name)
                df_player     = cleaning_transfermarkt_data(df_statistics)
                df_player     = df_player.drop(columns = ["Appearances"])
            except Exception:
                df_player     = pd.DataFrame(columns=column_names)


            
            
            dict_rename = {
                "Own Goals": "Autogoal",
                "Substitutions on": "Subentrato",
                "Substitutions off": "Sostituito",
                "Yellow cards": "Ammonito",
                "Second yellow cards": "Espulso Doppio Giallo",
                "Red Cards": "Espulsione diretta",
                "Penalty goals": "Goal su rigore",
                "MInutes per goal": "Minuti per Goal",
                "Minutes played": "Minuti Giocati",
                "Goals conceded": "Goal subiti", 
            }

            df_player = df_player.rename(columns= dict_rename)

            df_player     = df_player[df_player.Competizione.isin(competizioni)]


            for c in column_names:
                if c not in df_player.columns:
                    df_player[c] = 0
            


            if df_player.shape[0] > 0:
                for index, row in df_player.iterrows():
                    # check se i dati del giocatore sono già presenti nel modello, se no aggiungere al modello
                    if not FullStatistics.objects.filter(id_player = player_id, stagione = row["Stagione"]).exists():
                        # creazione nuovo record in Full Statistics
                        FullStatistics.objects.create(
                            id_player               = player_instance, 
                            stagione                = row["Stagione"],
                            club                    = row['Club'],
                            presenze                = row['Presenze'],
                            goal                    = row['Goals'],
                            assist                  = row['Assists'],
                            autogoal                = row['Autogoal'],
                            subentrato              = row['Subentrato'],
                            sostituito              = row['Sostituito'],
                            ammonizioni             = row['Ammonito'],
                            espulsioni_doppiogiallo = row['Espulso Doppio Giallo'],
                            espulsioni_dirette      = row['Espulsione diretta'],
                            rigori_segnati          = row['Goal su rigore'],
                            minuti_pergoal          = row['Minuti per Goal'],
                            minuti_giocati          = row['Minuti Giocati'],
                            goal_subiti             = row["Goal subiti"],
                            clean_sheets            = row["Clean Sheets"]

                        )
                        self.stdout.write(self.style.SUCCESS(f"{player_name} statistiche transfermarkt ottenute per stagione {row['Stagione']}e inserite nel database"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Statistiche per {player_name} già presenti nel database per la stagione {row['Stagione']}"))
            else: 
                player_nostats.append(player_name)
                self.stdout.write(self.style.ERROR(f"{player_name} nessuna statistica trovata su transfermarkt (nelle competizioni selezionate)"))

        # Log dei giocatori per i quali non sono state ottenute statistiche
        if player_nostats:
            self.stdout.write(self.style.ERROR(f"Giocatori senza statistiche: {', '.join(player_nostats)}"))
