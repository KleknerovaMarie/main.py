# Engeto-3-projekt
Třetí projekt na Python Akademii od Engeta.



## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí je zde: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ 


## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

$ pip3 --version                         # ověřím verzi manažeru
$ pip3 install -r requirements.txt       # nainstalujeme knihovny

## Spouštění projektu

Spuštění souboru projekt3_engeto.py v rámci přík. řádku požaduje dva povinné argumenty.

   python projekt3_engeto.py <odkaz-územního-celku> <výsledný soubor>

Následně se vám stáhnou výsledky jako soubor s příponou .csv.

## Ukázka projektu

Výsledky hlasování pro okres Prostějov:

  1.argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
  2.argument: vysledky_prostejov.csv

Spuštění programu:

  python projekt3_engeto.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'vysledky_prostejov.csv'


