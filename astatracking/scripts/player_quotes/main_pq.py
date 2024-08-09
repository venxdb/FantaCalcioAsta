from astatracking import setup
import pandas as pd
setup()

from django.conf import settings
from astatracking.models import Player_Quotes



try:
    
    print("Importazione di settings riuscita!")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
except Exception as e:
    print(f"Errore nell'importazione o nell'uso di settings: {e}")


"""
    Funzione per pulire i dati delle quotazioni
"""
def get_cleaning_quotes():

    df            = pd.read_excel(f"{settings.STATICFILES_DIRS[0]}/player_quotes/Quotazioni.xlsx", sheet_name = "Tutti", skiprows = 1)
    df            = df[["Id", "R", "Nome", "Squadra", "Qt.A", "Qt.I"]]
    df.columns    = ["Id", "Ruolo", "Nome", "Squadra", "Quotazione_Attuale", "Quotazione_Iniziale"]

    renaming_rols = {
                        "P": "Portiere",
                        "D": "Difensore",
                        "C": "Centrocampista",
                        "A": "Attaccante"
                    }

    df["Ruolo_Full"] = df.Ruolo.apply(lambda x: renaming_rols[x])
    df = df[["Id", "Ruolo", "Ruolo_Full", "Nome", "Squadra", "Quotazione_Attuale", "Quotazione_Iniziale"]]

    return df

"""
    Funzione per caricare i dati nella tabella Player_Quotes
"""


def load_data_to_db(dataframe):

    for _, row in dataframe.iterrows():

        Player_Quotes.objects.create(
            id                  = row['Id'],
            ruolo               = row['Ruolo'],
            ruolo_desc          = row["Ruolo_Full"],
            nome                = row["Nome"],
            squadra             = row['Squadra'],
            quotazione_attuale  = row['Quotazione_Attuale'],
            quotazione_iniziale = row['Quotazione_Iniziale']
        )


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


