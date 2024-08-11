

from functions_pq import *
from astatracking.models import Player_Quotes
import pandas as pd







if __name__ == "__main__":
    df = get_cleaning_quotes()

    num_players = Player_Quotes.objects.count()
    Player_Quotes.objects.all().delete()
    print(f"-- Cancellate vecchie quotazioni. N° istanze cancellate: {num_players}")
    num_players = Player_Quotes.objects.count()
    print(f"-- N° istanze post cancellazione: {num_players}")

    print("\nInizio caricamento quotazioni")
    load_data_to_db(df)
    num_players = Player_Quotes.objects.count()
    print(f"-- Numero di giocatori inseriti in tabella: {num_players}")


