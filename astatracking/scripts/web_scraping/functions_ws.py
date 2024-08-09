from bs4 import BeautifulSoup
import requests
import pandas as pd

"""
    Funzione per ottenere i dati statistici in formato tabellare.
"""
def get_cell_data(td):
    a_tag = td.find('a')
    if a_tag and 'title' in a_tag.attrs and a_tag.text == '':
        return a_tag['title']
    else:
        return td.text.strip()
    

"""
    Funzione per ottenere il link dove si trovano le statistiche dettagliate
"""

def get_detailed_statistics_link(player_name, headers):

    player_name = player_name.lower().replace(" ", "+")
    search_url  = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={player_name}"

    response    = requests.get(search_url, headers = headers)
    soup        = BeautifulSoup(response.text, 'html.parser')

    base_link           = "https://www.transfermarkt.com"
    player_link         = soup.find('td', class_ = "hauptlink").find('a')
    full_link_extracted = base_link + player_link['href']

    stats_link_word     = "leistungsdatendetails"
    stats_full_link     = full_link_extracted.replace("profil", stats_link_word)

    response_stats_full_link         = requests.get(stats_full_link, headers = headers)
    soup                             = BeautifulSoup(response_stats_full_link.text, 'html.parser')
    detailed_stats_link_html_element = soup.find('a', class_ = "tm-tab", string = "Detailed")
    full_detailed_stats_link         = base_link + detailed_stats_link_html_element['href']

    return full_detailed_stats_link

"""
    Funzione per ottenere le statistiche dettagliate del giocatore
"""

def get_statistics_player(player_name):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    detailed_stats_link = get_detailed_statistics_link(player_name, headers)
    response            = requests.get(detailed_stats_link, headers = headers)
    soup                = BeautifulSoup(response.text, 'html.parser')
    table_stats         = soup.find("table", class_ = "items")

    data = []
    for row in table_stats.find_all('tr')[1:]:
        row_data = [get_cell_data(td) for td in row.find_all('td')]
        if row_data[0] != '':
            row_data.pop(1)
            data.append(row_data)
    
    column_names = ["Stagione", "Competizione", "Club", "Convocazioni", "Presenze", "Punti per match", "Goals",
                    "Assists", "Autogoal",
                    "Subentrato", "Sostituito", "Ammonito", "Espulso Doppio Giallo", "Espulsione diretta",
                    "Gol su rigore",
                    "Minuti per Goal", "Minuti Giocati"]
    
    df           = pd.DataFrame(data, columns = column_names)
    df.insert(0, "Giocatore", player_name)
    
    return df

def cleaning_transfermarkt_data(dataframe: pd.DataFrame):

    not_int_cols = ["Giocatore", "Stagione", "Competizione", "Club"]
    for col in dataframe.columns:
        if col not in not_int_cols:
            dataframe[col] = dataframe[col].apply(lambda x: x.replace("-", "0").replace("'", ""))
            if col != "Punti per match":
                dataframe[col] = dataframe[col].apply(lambda x: x.replace(".", ""))
                dataframe[col] = dataframe[col].astype(int)
            else:
                dataframe[col] = dataframe[col].apply(lambda x: x.replace(",", "."))
                dataframe[col] = dataframe[col].astype(float)

    return dataframe


