import pandas as pd

def get_cleaning_quotes():

    df            = pd.read_excel("data/quotazioni/Quotazioni.xlsx", sheet_name = "Tutti", skiprows = 1)
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
    Funzione per salvare i dati presenti nella tabella Quotazioni
"""
def populate_quotes_table(dataframe: pd.DataFrame):

    df = dataframe