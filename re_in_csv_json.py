import re
import csv
import json
import os

#vzorec bloka 
#vzorec_bloka = re.compile(
 #   r'<div class"table_wrapper tabbed" id="all_per_game_stats">'
  #  r''
   # flags=re.DOTALL
#) 


#vzorec_igralec = re.compile()

html_datoteka = "stran.html"
csv_regular = "redni_del_sezone.csv"
json_regular = "redni_del_sezone.json"
csv_playoffs = "koncnica.csv"
json_playoffs = "koncnica.json"



def preberi_besedilo_iz_html(mapa, datoteka):
    path = os.path.join(mapa, datoteka)
    with open(path, "r", encoding="utf-8") as dat:
        return dat.read()
    

def rednidel_sezone(html):
    vzorec_rednidelsezone = r'<div class="table_container tabbed current hide_long long" id="div_per_game_stats">(.*?)<\/div>'   #<div class="table_container tabbed current hide_long long" id="div_per_game_stats">
    najdi_rednidel = re.search(vzorec_rednidelsezone, html, flags=re.DOTALL)
    if najdi_rednidel:
        return najdi_rednidel.group(1)
    else:
        return ""
    
def playoffs(html):
    vzorec_playoffs = r'<div class="table_container tabbed hide_long long" id="div_per_game_stats_post">(.*?)<\/div>'   #<div class="table_container tabbed hide_long long" id="div_per_game_stats_post">
    najdi_playoffs = re.search(vzorec_playoffs, html, flags=re.DOTALL)
    if najdi_playoffs:
        return najdi_playoffs.group(1)
    else:
        return ""
    
def izlusci_kategorije(html):
    vzorec_kategorij = r'<thead>(.*?)<\/thead>'
    vzorec_kategorije = r'<th .*?>(.*?)<\/th>'
    iskane_kategorije = ["Rank", "Player", "Age", "Team", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
    
    najdi_kategorije = re.search(vzorec_kategorij, html, flags=re.DOTALL)
    if najdi_kategorije:
        vse_kategorije = re.findall(vse_kategorije, najdi_kategorije.group(1), flags=re.DOTALL)
        preciscene_kategorije = []
        for kategorija in vse_kategorije:       #pobrišemo morebitne presledke
            preciscene_kategorije.append(kategorija.strip())
        #filtriramo vse kategorije, da dobimo le tiste katere želimo (iskane kategorije)
        izbrane_kategorije = []
        for kategorija in preciscene_kategorije:
            if kategorija in iskane_kategorije:
                izbrane_kategorije.append(kategorija)
        return izbrane_kategorije
    return []

st_kategorij = len(izlusci_kategorije(html_datoteka))

def izlusci_igralce(html):
    vzorec_igralci = r'<tbody>(.*?)<\/tbody>'       # v kakšni obliki najdemo VSE igralce v html kodi
    vzorec_igralec = r'<tr .*?>(.*?)<\/tr>'         # v kakšni obliki najdemo ENEGA igralca v html kodi
    vzorec_vrednosti = r'<td .*?>(.*?)<\/td>'       # v kakšni obliki najdemo statistiko za vsakega igralca v html kodi
    najdi_igralce = re.search(vzorec_igralci, html, flags=re.DOTALL)      #imamo kodo, kjer so zajeti vsi igralci
    podatki_o_igralcu = [] 
    if najdi_igralce:
        najdi_igralca = re.findall(vzorec_igralec, najdi_igralce.group(1), flags=re.DOTALL)    #dobili smo kodo za enega igralca
        for vrstica in najdi_igralca:
            vrednosti = re.findall(vzorec_vrednosti, vrstica, flags=re.DOTALL)
            if vrednosti:
                preciscene_vrednosti = []
                for v in vrednosti:
                    preciscene_vrednosti.append(v.strip())
                
                if len(preciscene_vrednosti) == st_kategorij - 1:  # Če je ena vrednost premalo
                    preciscene_vrednosti.insert(0, '')  # Dodamo prazno vrednost na prvo mesto

                podatki_o_igralcu.append(preciscene_vrednosti)
    return podatki_o_igralcu
                    





def ustvari_seznam_slovarjev(html):
    seznam_slovarjev = []      #seznam slovarjev, ključi so kategorije, vrednosti pa podatki za vsakega igralca
    kategorije = izlusci_kategorije(html)
    podatki_o_igralcih = izlusci_igralce(html)
    for podatki in podatki_o_igralcih:
        igralec_slovar = dict(zip(kategorije, podatki))
        seznam_slovarjev.append(igralec_slovar)
    
    return seznam_slovarjev






def obdelaj_regular_season(html):
    regular_season_html = rednidel_sezone(html)
    if regular_season_html:
        kategorije = izlusci_kategorije(regular_season_html)
        podatki = izlusci_igralce(regular_season_html)
        return kategorije, podatki
    return [], []

def obdelaj_playoffs(html):
    playoffs_html = playoffs(html)
    if playoffs_html:
        kategorije = izlusci_kategorije(playoffs_html)
        podatki = izlusci_igralce(playoffs_html)
        return kategorije, podatki
    return [], []


#def rednidel_csv(regularseason_csv, seznam_slovarjev, kategorije):
 #   with open(regularseason_csv, "w", encoding="utf-8") as csv_datoteka:
  #      writer = csv.DictWriter(csv_datoteka, fieldnames=kategorije)
   #     writer.writeheader()
    #    writer.writerows(igralci)




# funkcija, ki obdela regular season 

# funkcija, ki obdela playoffs

# nardis csv in json datoteki za regular season
# nardis csv in json datoteki za playoffse


#with open("podatki.csv", "w") as f:
 #   pisi = csv.writer(f)
  #  pisi.writerow(["ime", "položaj", "odigrane tekme", "PPG", "APG", "RPG", "FG%", "3PT%", "FT%"])

