import requests
import os
import csv
import json
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
def preberi_besedilo_iz_html(mapa, datoteka):
    path = os.path.join(mapa, datoteka)
    with open(path, "r", encoding="utf-8") as dat:
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

