#  Elections Scraper

## Funkce programu
Program získává data z voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017 prostřednictvím webových stránek: `https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ`
Výsledky jsou uloženy v souboru .csv. 
Pro spuštění programu je zapotřebí vybrat volební obvod z webových stránek, (např. `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103` pro volební obvod prostějov) a nastavit jméno souboru (např. `vysledky_voleb_prostejov.csv`)

## Instalace knihoven
Knihovny, které jsou zapotřebí ke spuštění programu najdete v souboru `requirement.txt`
instalace knihoven můžete udělat pomocí příkazového řádku:
```
pip3 install -r requirements.txt
```

## Spuštění programu
Ke spuštění peogramu je potřeba 2 argumenty ve správném pořadí a to první odkaz na stránky a druhý název csv souboru
```pyrhon
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_voleb_prostejov.csv"
```
## Výsledek
Výsledkem je soubor `vysledky_voleb_prostejov.csv`, který si můžete prohlédnout ve složce projektu. 
