import pandas as pd
from django.conf import settings
from astatracking.models import Player_Quotes
import os

"""
    Funzione per pulire i dati delle quotazioni
"""
def get_cleaning_quotes():


    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'player_quotes', 'Quotazioni.xlsx')

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Il file {file_path} non esiste.")
    
    df            = pd.read_excel(file_path, sheet_name="Tutti", skiprows=1)
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