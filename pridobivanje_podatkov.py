import requests
import re
import csv
import json
import os
from bs4 import BeautifulSoup

#url spletne strani
brstats_url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
#datoteka, kjer bomo shranili html spletne strani
brstats_html = "stran.html"
#datoteka, kjer bomo shranili podatke iz spletne strani v csv
brstats_csv = "podatki.csv"
#mapa s podatki
direktorij = "podatki"


#funkcija, ki prejme url spletne strani in naredi datoteko z HTML kodo spletne strani
def shrani_url_v_html_datoteko(url, datoteka):
    try:
        vsebina = requests.get(url)
        if vsebina.status_code == 200:
            vsebina_utf8 = vsebina.content.decode("utf-8")
            with open(datoteka, "w", encoding="utf-8") as dat:
                dat.write(vsebina_utf8)
                print("Datoteka je shranjena.")
    except:
        print(f"Napaka pri nalaganju URL-ja {url}")
        return None
    return vsebina_utf8


#prebere niz z vsebino datoteke
def preberi_besedilo_iz_html(datoteka):
    #path = os.path.join(mapa, datoteka)
    with open(datoteka  , "r", encoding="utf-8") as dat:
        return dat.read()
    

#funkcija, ki prejme datoteko z neurejeno html kodo in jo uredi
def uredi_html(datoteka):
    with open(datoteka, "r", encoding="utf-8") as dat:
        soup = BeautifulSoup(dat, "html.parser")
        urejen_html = soup.prettify()
        with open(datoteka, "w", encoding="utf-8") as dat:
            dat.write(urejen_html)
            print("Urejena HTML koda je bila prepisana.")


shrani_url_v_html_datoteko(brstats_url, brstats_html)
uredi_html(brstats_html)



html_datoteka = "stran.html"
csv_regular = "redni_del_sezone.csv"
json_regular = "redni_del_sezone.json"
csv_playoffs = "koncnica.csv"
json_playoffs = "koncnica.json"



def regular_season(html):
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
    #iskane_kategorije = ["Player", "Age", "Team", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "Awards"]
    napacen_eFG = 'Effective Field Goal Percentage</strong><br>This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal." data-filter="1" data-name="" >eFG%'
    pravilen_eFG = "eFG%"
    najdi_kategorije = re.search(vzorec_kategorij, html, flags=re.DOTALL)
    if najdi_kategorije:
        vse_kategorije = re.findall(vzorec_kategorije, najdi_kategorije.group(1), flags=re.DOTALL)
        preciscene_kategorije = []
        for kategorija in vse_kategorije:       #pobrišemo morebitne presledke
            preciscene_kategorije.append(kategorija.strip())
        #filtriramo vse kategorije, da dobimo le tiste katere želimo (iskane kategorije)
        #izbrane_kategorije = []
        #for kategorija in preciscene_kategorije:
         #   if kategorija in iskane_kategorije:
          #      izbrane_kategorije.append(kategorija)
        #return izbrane_kategorije
        for i in range(len(preciscene_kategorije)):
            if preciscene_kategorije[i] == napacen_eFG:
                preciscene_kategorije[i] = pravilen_eFG
        if len(preciscene_kategorije) > 1:
           preciscene_kategorije = preciscene_kategorije[1:]  # odstranimo rank
        return preciscene_kategorije
    return []

#st_kategorij = len(izlusci_kategorije(brstats_html))


def izlusci_igralce(html):
    vzorec_igralci = r'<tbody>(.*?)<\/tbody>'       # v kakšni obliki najdemo VSE igralce v html kodi
    vzorec_igralec = r'<tr .*?>(.*?)<\/tr>'         # v kakšni obliki najdemo ENEGA igralca v html kodi
    vzorec_vrednosti = r'<td .*?>(.*?)<\/td>'       # v kakšni obliki najdemo statistiko za vsakega igralca v html kodi
    vzorec_imena = r'<a href="/players/.*?>(.*?)<\/a>'          # vzorec za ime, da pobrišemo dodatne značke okoli imena
    najdi_igralce = re.search(vzorec_igralci, html, flags=re.DOTALL)      #imamo kodo, kjer so zajeti vsi igralci
    podatki_o_igralcih = []

    if najdi_igralce:
        najdi_igralca = re.findall(vzorec_igralec, najdi_igralce.group(1), flags=re.DOTALL)    #dobili smo kodo za enega igralca
        for vrstica in najdi_igralca:
            vrednosti = re.findall(vzorec_vrednosti, vrstica, flags=re.DOTALL)
            if vrednosti:
                preciscene_vrednosti = []
                for v in vrednosti:
                    najdi_ime = re.search(vzorec_imena, v, flags=re.DOTALL)
                    if najdi_ime:
                        ime_igralca = najdi_ime.group(1).strip()
                        preciscene_vrednosti.append(ime_igralca)
                    else:
                        brez_ostalih_oznak = re.sub(r'<.*?>', '', v).strip()
                        preciscene_vrednosti.append(brez_ostalih_oznak)

                podatki_o_igralcih.append(preciscene_vrednosti)

    #for podatki_o_enem_igralcu in podatki_o_igralcih:           #iz podatkov o igralcih zbrišemo 
     #   if len(podatki_o_enem_igralcu) > 16:                    #vrednosti za eFG% na 17.mestu
      #      del podatki_o_enem_igralcu[16]

    return podatki_o_igralcih
                    

#funkcija, ki ustvari seznam slovarjev, kjer ključi kategorije, vrednosti pa podatki za vsakega igralca
def ustvari_seznam_slovarjev(html):
    seznam_slovarjev = []      
    kategorije = izlusci_kategorije(html)
    podatki_o_igralcih = izlusci_igralce(html)
    for podatki in podatki_o_igralcih:
        igralec_slovar = dict(zip(kategorije, podatki))
        seznam_slovarjev.append(igralec_slovar)
    
    return seznam_slovarjev


# funkcija za zapis podatkov v csv
def naredi_csv(datoteka_csv, seznam_slovarjev, kategorije):
    with open(datoteka_csv, "w", encoding="utf-8") as dat:
        writer = csv.DictWriter(dat, fieldnames=kategorije)
        writer.writeheader()
        for igralec in seznam_slovarjev:
            writer.writerow(igralec)


# funkcija za zapis podatkov v json
def naredi_json(datoteka_json, seznam_slovarjev):
    with open(datoteka_json, "w", encoding="utf-8") as dat:
        json.dump(seznam_slovarjev, dat, ensure_ascii=False, indent=4)


# funkcija, ki obdela regular season 
def obdelaj_regular_season(html, csv_datoteka, json_datoteka):
    regular_season_html = regular_season(html)
    if regular_season_html:
        seznam_slovarjev = ustvari_seznam_slovarjev(regular_season_html)
        kategorije = izlusci_kategorije(regular_season_html)
    naredi_csv(csv_datoteka, seznam_slovarjev, kategorije)
    naredi_json(json_datoteka, seznam_slovarjev)


# funkcija, ki obdela playoffs
def obdelaj_playoffs(html, csv_datoteka, json_datoteka):
    playoffs_html = playoffs(html)
    if playoffs_html:
        seznam_slovarjev = ustvari_seznam_slovarjev(playoffs_html)
        kategorije = izlusci_kategorije(playoffs_html)
    naredi_csv(csv_datoteka, seznam_slovarjev, kategorije)
    naredi_json(json_datoteka, seznam_slovarjev)


#funkcija, ki prejme html datoteko in posebej obdela stran za redni del in končnico
def obdelaj_shrani_vse(html_datoteka, csv_regular, json_regular, csv_playoffs, json_playoffs):
    html = preberi_besedilo_iz_html(html_datoteka)
    obdelaj_regular_season(html, csv_regular, json_regular)
    obdelaj_playoffs(html, csv_playoffs, json_playoffs)



#html = preberi_besedilo_iz_html(direktorij, brstats_html)

print(izlusci_kategorije(shrani_url_v_html_datoteko(brstats_url, brstats_html)))
print(izlusci_igralce(shrani_url_v_html_datoteko(brstats_url, brstats_html)))

obdelaj_shrani_vse(html_datoteka, csv_regular, json_regular, csv_playoffs, json_playoffs)




# nardis csv in json datoteki za regular season
# nardis csv in json datoteki za playoffse

