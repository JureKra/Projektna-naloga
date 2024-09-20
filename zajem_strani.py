import requests
import os


#url spletne strani
sistat_url = "https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/2640010S.px/table/tableViewLayout1/"
#datoteka, kjer bomo shranili html spletne strani
sistat_html = "stran.html"
#datoteka, kjer bomo shranili podatke iz spletne strani v csv
sistat_csv = "podatki.csv"
#mapa s podatki
direktorij = "podatki"


def url_v_niz(url):
    try:
        vsebina = requests.get(url)
        if vsebina.status_code == 200:
            return vsebina.text
    except:
        print(f"Napaka pri nalaganju URL-ja {url}")
        return None
    return vsebina.text


def url_v_html_datoteko(text, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    path = os.path.join(mapa, datoteka)
    with open(path, "w", encoding="utf-8") as dat:
         dat.write(text)


def preberi_besedilo_iz_html(mapa, datoteka):
    path = os.path.join(mapa, datoteka)
    with open(path, "r", encoding="utf-8") as dat:
        return dat.read()
    


url_v_niz(sistat_url) 
url_v_html_datoteko(url_v_niz(sistat_url), direktorij, sistat_html)