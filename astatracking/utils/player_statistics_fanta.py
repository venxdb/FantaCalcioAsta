import pandas as pd
import os
from django.conf import settings

from astatracking.models import StatisticheFanta

def get_statistics_year(filepath, season):
    
    renaming_cols_dict = {
            "R": "Ruolo",
            "Pv": "PartiteAVoto", "Mv": "MediaVoto", "Fm": "FantaMedia",
            "Gf": "GoalFatti", "Gs": "GoalSubiti", "Rp": "RigoriParati",
            "Rc": "RigoriCalciati", "R+": "RigoriSegnati", "R-": "RigoriSbagliati",
            "Ass": "Assist", "Amm": "Ammonizioni", "Esp": "Espulsioni", "Au": "Autogoal"
        }

    cols_to_drop        = ["Id", "Rm"]

    df              = pd.read_excel(filepath, sheet_name = "Tutti", skiprows = 1)
    df              = df.rename(columns = renaming_cols_dict)
    df              = df.drop(columns = cols_to_drop)
    columns_df      = df.columns.to_list()

    df["Stagione"]  = season
    columns_to_take = ["Stagione"] + columns_df

    df              = df[columns_to_take]

    return df

    



