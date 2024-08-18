from django.core.management.base import BaseCommand
from astatracking.utils.player_statistics_fanta import get_statistics_year
from astatracking.models import Player_Quotes, StatisticheFanta
import pandas as pd
import os

from django.conf import settings

class Command(BaseCommand):

    help = "Aggiorna le statistiche fantacalcio"

    def handle(self, *args, **options):

        folder_path = os.path.join(settings.STATICFILES_DIRS[0], "statistics/leghe")

        files = os.listdir(folder_path)

        df_statitistics = pd.DataFrame()

        for file in files:
            stagione1   = file.replace(".xlsx", "").split("_")[-2]
            stagione2   = file.replace(".xlsx", "").split("_")[-1]
            stagione    = f"{stagione1}/20{stagione2}"

            full_path       = folder_path + "/" + file
            df              = get_statistics_year(full_path, stagione)
            df_statitistics = pd.concat([df_statitistics, df])
            
        df_statitistics     = df_statitistics.sort_values(by = ["Nome", "Stagione"])
        

        # dropping old statistics
        n_stat_presenti     = StatisticheFanta.objects.count()
        StatisticheFanta.objects.all().delete()
        string_output       = f"Cancellate {n_stat_presenti} statistiche dal database. [Pre - Inserimento]"
        self.stdout.write(self.style.SUCCESS(string_output))

        # loading statistics
        giocatori_nomi      = Player_Quotes.objects.values_list('nome', flat=True)
        filtered_statistics = df_statitistics[df_statitistics.Nome.isin(giocatori_nomi)]
        print(filtered_statistics.info())


        players     = Player_Quotes.objects.all()
        player_dict = {player.id: player for player in players}

        for player_id, player_instance in player_dict.items():

            player_name            = player_instance.nome

            df_statistics_player = df_statitistics[df_statitistics.Nome == player_name]

            if df_statistics_player.shape[0] > 0:
                
                for index, row in df_statistics_player.iterrows():
                    if not StatisticheFanta.objects.filter(giocatore = player_id, stagione = row["Stagione"]).exists():
                        StatisticheFanta.objects.create(
                            giocatore       = player_instance,
                            ruolo           = row["Ruolo"],
                            stagione        = row["Stagione"],
                            squadra         = row["Squadra"],
                            partiteavoto    = row["PartiteAVoto"],
                            mediavoto       = row["MediaVoto"],
                            fantamedia      = row["FantaMedia"],
                            goalfatti       = row["GoalFatti"],
                            goalsubiti      = row["GoalSubiti"],
                            rigoriparati    = row["RigoriParati"],
                            rigoricalciati  = row["RigoriCalciati"],
                            rigorisegnati   = row["RigoriSegnati"],
                            rigorisbagliati = row["RigoriSbagliati"],
                            assist          = row["Assist"],
                            ammonizioni     = row["Ammonizioni"],
                            espulsioni      = row["Espulsioni"],
                            autogoal        = row["Autogoal"]
                        )

                        statistics_message_post = f"Statistiche fantacalcio per {player_name} inserite a database per la stagione {row['Stagione']}"
                        self.stdout.write(self.style.SUCCESS(statistics_message))
                    else: 
                        statistics_message_post = f"Statisithce fantacalcio per {player_name} già presenti a database per la stagione {row['Stagione']}"
                        statistics_message = statistics_message + "\n" + statistics_message_post
                        self.stdout.write(self.style.WARNING(statistics_message))

            else:
                statistics_message = f"Statistiche Fantacalcio non presenti per {player_name}"
                self.stdout.write(self.style.WARNING(statistics_message))

            