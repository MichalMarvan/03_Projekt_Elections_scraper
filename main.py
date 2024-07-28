import requests
from bs4 import BeautifulSoup
import csv
import sys

"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Michal Marvan
email: marvan.michal@gmail.com
discord: Michal_M
"""

def kontrola_zadani(url: str, soubor: str):
    if "https://volby.cz/pls/ps2017nss" not in url or not soubor.endswith(".csv"):
        print("Špatné zadání, ukončuji program.")
        exit()
    else:
        print("Spouštím program.")

def ziskani_html(url: str) -> BeautifulSoup:
    """
    Funkce získá text HTML ze stránky.
    """
    odp_serveru = requests.get(url)# zápis url jako str
    return BeautifulSoup(odp_serveru.text, 'html.parser') # převedení HTML na text  

def vyber_atributy_z_radku(tr_tag: "bs4.element.ResultSet") -> list:
    """
    Získání informací o kódu obce a jména obce.
    """
    ## ze všech tr získáme text - číslo/kód obce [0] a jméno obce [1]
    return [
        tr_tag[0].getText(),  # cislo obce
        tr_tag[1].getText()   # jmeno obce
    ]

def vyber_atributy_volici(tr_tag: "bs4.element.ResultSet") -> list:
    """
    Získání informací z tabulky voličů. 
    """
    ## ze všech tr získáme text - pocet voličů [3], vydané obálky [4] a platné hlasy [7]
    ## zároveň jsou texty upraveny tak, aby rozdělovač ticísů byl nahrazen a číslo bylo jendotné
    return [
        tr_tag[3].getText(),  # pocet voličů
        tr_tag[4].getText(),  # vydané obálky
        tr_tag[7].getText()   # platné hlasy
    ]

def vyber_atributy_strany(tr_tag: "bs4.element.ResultSet") -> list:
    """
    Získání informací o politické straně a počtu hlasů.
    """
    ## ze všech tr získáme text - nazev strany [1] a počet hlasů strany [2]
    ## zároveň jsou texty upraveny tak, aby rozdělovač ticísů byl nahrazen a číslo bylo jendotné
    return [
        tr_tag[1].getText(),  # nazev strany
        tr_tag[2].getText()   # platne hlasy celkem
    ]

def ziskat_odkazy(soup) -> list:
    """
    Získejte všechny odkazy z tabulky, které obsahují kódy obcí.
    """
    table = soup.find("div", {"id": "inner"})
    vsechny_tr = table.find_all("tr")
    odkazy_seznam = []
    
    for prvek in vsechny_tr[2:]:    # [2:0] pro zbavení se hlavičky
        vsechny_a_tagy = prvek.find_all("a")
        for a_tag in vsechny_a_tagy:
            href = a_tag.get('href')
            if href:
                cely_odkaz = "https://volby.cz/pls/ps2017nss/" + href
                odkazy_seznam.append(cely_odkaz)
                break
    # pod kódy obcí jsou odkazy, které ukrývajíé další tabulky, jak se v dané obci hlasovalo
    return odkazy_seznam

def ziskat_data_obce(vsechny_tr) -> list:
    """
    Získejte data o obcích.
    """
    vysledky_obci = []
    for tr in vsechny_tr[2:]:
        td_na_radku = tr.find_all("td")
        if td_na_radku:
            data_obce = vyber_atributy_z_radku(td_na_radku)
            vysledky_obci.append(data_obce)
    # získání kódu obcí a jména obcí        
    return vysledky_obci

def ziskat_vysledky_strany(vsechny_tr) -> tuple:
    """
    Získejte výsledky jednotlivých stran.
    """
    vysledky_strany = []
    nazvy_stran = set()

    for tr in vsechny_tr:
        obecni_vysledky = {}
        for jedno_tr in tr:    
            td_na_radku = jedno_tr.find_all("td")
            if td_na_radku and td_na_radku[1].getText() != "-":
                data_strany = vyber_atributy_strany(td_na_radku)
                nazev_strany = data_strany[0]
                hlasy = data_strany[1]
                nazvy_stran.add(nazev_strany)
                obecni_vysledky[nazev_strany] = hlasy
        vysledky_strany.append(obecni_vysledky)
    # výsledky (hlasy) jednotlivých stran a seznam (set()) všech stran
    return vysledky_strany, nazvy_stran

def ziskat_vysledky_volici(vsechny_tr) -> list:
    """
    Získejte výsledky voličů.
    """
    vysledky_volicu = []
    for tr in vsechny_tr[2:]:
        for jedno_tr in tr:    
            td_na_radku = jedno_tr.find_all("td")
            if td_na_radku:
                vysledky_volicu.append(vyber_atributy_volici(td_na_radku))
    # datak k voličům z funkce: vyber_atributy_volici()
    return vysledky_volicu

def odstranit_znaky(data) -> list:
    """
    Odstraní nechtěné znaky z dat.
    """
    opraveny_seznam = []
    for itemy in data:
        podseznam = [item.replace('\xa0', '') for item in itemy]
        opraveny_seznam.append(podseznam)
    return opraveny_seznam

def zapis_do_csv(vystupni_soubor, hlavicka, data):
    """
    Zapíše data do CSV souboru.
    """
    with open(vystupni_soubor, mode="w", newline='', encoding='utf-8') as nove_csv:
        zapisovac = csv.writer(nove_csv)
        zapisovac.writerow(hlavicka)    # zápis hlavičky tabulky
        for row in data:
            zapisovac.writerow(row)     # Zápis všech ostatních dat

def hlavni(url, vystupni_soubor):
    kontrola_zadani(url, vystupni_soubor)
    soup = ziskani_html(url)
    vsechny_tr = soup.find("div", {"id": "inner"}).find_all("tr")
    
    vysledky_obce = ziskat_data_obce(vsechny_tr)
    odkazy = ziskat_odkazy(soup)
    
    vsechny_tr_strany = []
    vsechny_tr_volici = []
    for hodne_url in odkazy:
        soup_2 = ziskani_html(hodne_url)
        vsechny_tr_strany.append(soup_2.find("div", {"id": "inner"}).find_all("tr"))
        vsechny_tr_volici.append(soup_2.find("table", {"class": "table"}).find_all("tr"))

    vysledky_strany, nazvy_stran = ziskat_vysledky_strany(vsechny_tr_strany)
    vysledky_volici = ziskat_vysledky_volici(vsechny_tr_volici)
    opraveny_volici = odstranit_znaky(vysledky_volici)

    hlavicka = ["kod obce", "jmeno obce", "pocet volicu", "vydane obalky", "platne hlasy"] + list(nazvy_stran)
    data = []
    for obec, volici_data, vysledky_obce in zip(vysledky_obce, opraveny_volici, vysledky_strany):
        row = obec + volici_data
        for nazev_strany in nazvy_stran:
            row.append(vysledky_obce.get(nazev_strany, 0))
        data.append(row)
    
    zapis_do_csv(vystupni_soubor, hlavicka, data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití skriptu: python main.py <url> <vystupni_soubor>")
        sys.exit(1)

    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    
    hlavni(url, vystupni_soubor)
