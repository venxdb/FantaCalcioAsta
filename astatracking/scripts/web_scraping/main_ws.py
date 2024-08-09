from functions_ws import *


"""
    Funzione main per estrarre le statistiche dettagliate da transfermarkt (web scraping)
"""

def main_ws_statistic(player_name):
    
    df_statistics = get_statistics_player(player_name)
    df_player     = cleaning_transfermarkt_data(df_statistics)

    return df_player


df_statistics = get_statistics_player("Douglas Luiz")
df_player     = cleaning_transfermarkt_data(df_statistics)

print(df_player)

