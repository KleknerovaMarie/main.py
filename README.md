# Engeto-3-projekt
Třetí projekt na Python Akademii od Engeta.



## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí je zde: 
https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ 


## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```markdown
$ pip3 --version                         # ověřím verzi manažeru

$ pip3 install -r requirements.txt       # nainstalujeme knihovny
```

## Spouštění projektu

Spuštění souboru projekt3_engeto.py v rámci přík. řádku požaduje dva povinné argumenty.

   `python projekt3_engeto.py <odkaz-územního-celku> <výsledný soubor>`

Následně se vám stáhnou výsledky jako soubor s příponou .csv.

## Ukázka projektu

**Výsledky hlasování pro okres Prostějov:**
```markdown
1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103

2. argument: vysledky_prostejov.csv
```



**Spuštění programu:**
```markdown
python projekt3_engeto.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'vysledky_prostejov.csv'
```




**Průběh stahování:**
```markdown
Stahuji data z vybraného URL:https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103

Ukládám do souboru: vysledky_prostejov.csv

Ukončuji election_scraper
```



**Částečný výstup:**
```markdown
code|location|registered|envelopes|valids|Občanská demokratická strana|Řád národa - Vlastenecká....... 
506761|Alojzov|205|145|144|29|0|0|9|0|5|17|4|1|1|0|0|18|0|5|32|0|0|6|0|0|1|1|15|0
589268|Bedihošť|834|527|524|51|0|0|28|1|13|123|2|2|14|1|0|34|0|6|140|0|0|26|0|0|0|0|82|1
589276|Bílovice-Lutotín|431|279|275|13|0|0|32|0|8|40|1|0|4|0|0|30|0|3|83|0|0|22|0|0|0|1|38|0
589284|Biskupice|238|132|131|14|0|0|9|0|5|24|2|1|1|0|0|10|2|0|34|0|0|10|0|0|0|0|19|0
........
```



