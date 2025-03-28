"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Marie Kleknerová
email: racanovamarie@gmail.com
"""



import requests
from bs4 import BeautifulSoup as bs
import argparse
import csv
import pandas as pd









parser = argparse.ArgumentParser()



# kontrola jestli argparse celek je v seznamu URL adres
def parsers_celek(celek,okresy:list):
    if not celek or celek not in okresy:
        return False
    
    else:
        return True

# kontrola jestli argparse file_name má příponu .csv
def parsers_name(name_file:str):
    return bool(name_file) and name_file.endswith('.csv')

    
#všechny tr tagy, můžu použít u obou stránek
def tr_tag(url_adress):
    vsechny_tr_tagy = soup.find_all("tr")[2:]
    return vsechny_tr_tagy


#všechny a tagy, můžu použít u obou stránek
def a_tag(url_adress):
    a_tags = []
    vsechny = soup.find_all("a")
    for kus in vsechny:
        j = a_tags.append(kus.get("href"))
    return a_tags


#všechny url adresy, lze použít jen u první stránky
def district(every_atag):
    first_links = []
    for c in every_atag:
        c = str(c)
        if c[:4] == "ps32" or c[:5] == "ps36?":
            e = first_links.append("https://www.volby.cz/pls/ps2017nss/" + c)
        else:    
            continue
    return first_links


# názvy měst 
def list_name(tr_tag):
    okr = []
    for okres in tr_tag:
        jmena_okresu = okres.contents[3].text
        if jmena_okresu != "název" and jmena_okresu != "VýběrPM" and jmena_okresu != "Výběrokrsku" and jmena_okresu != "-":
            i = okr.append(jmena_okresu)
        else:
            continue
    return okr 



#td u druhé stránky, všechny td třídy číslo
def all_td(url_adress):
   every_td = soup.find_all("td", {"class": "cislo"}) 
   return every_td




# ahref u druhé stránky
def all_a(td):
   kr = []
   for dist in td:
      c = kr.append(dist.contents[0])
   return kr



# odkazy u druhé stránky
def link(every_a):
   links = []
   for d in every_a:
      d = str(d)
      u = d.replace("amp;", "")
      s = links.append("https://www.volby.cz/pls/ps2017nss/" + u[9:-12])
   
   return links


# odstraňuje pevné mezery u čísel
def cleaner(list_of_numbers):
    list_of_numbers = str(list_of_numbers)
    z = list_of_numbers.replace("\xa0", "")
    return z

# kody měst pro tabulku
def codes(td):
    code = []
    for t in td:
        cisla_mest = t.contents[1].text
        cisla_mest = str(cisla_mest)
        if cisla_mest.isalpha():                      #in ("kód", "Územní úroveň", "X", "-", "Obec", "číslo"):
            continue
        else:
            i = code.append(cisla_mest)
    return code


#údaje do tabulky 
def registered(url:str):
   
    people = soup.find("td", {"class": "cislo", "headers": "sa2"}).text
    human = cleaner(people)
    return human


#údaje do tabulky
def envelopes(url):
    envelope = soup.find("td", {"class": "cislo","headers": "sa3"}).text
    better = cleaner(envelope)
    return better


# údaje do tabulky
def valid(url):
    val = soup.find("td", {"class": "cislo", "headers": "sa6"}).text
    vali = cleaner(val)
    return vali


# seznam politických stran do tabulky
def political_parties(tr):
    politic = []
    for r in tr:
       z = r.contents[3].text
       z = str(z)
       if z in ("název", "Platné hlasy", "-") or z.isdigit():
           continue
       else:
        o = politic.append(z)
    politic = tuple(politic)
    return politic




# počet hlasů u jednotlivých politických stran do tabulky bez pevných mezer
def quantity(tr):
    many = []
    for cast in tr[3:-1]:
        cisla = cast.contents[5].text
        if cisla in ("Předn.hlasy", "celkem"):
            continue
        else:
          cisla = str(cisla)
          better_cisla = cleaner(cisla)
          i = many.append(better_cisla)
    return many




adress = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"


# odeslání požadavku GET
odpoved = requests.get(adress)
if odpoved.status_code != 200:
    quit()
else:

# parsování vráceného HTML souboru
    soup = bs(odpoved.text, features="html.parser")   



    parser.add_argument("url_adress", type=str,                                                                 # 1.argument pro zadání URL
                        help="Napiš url odkaz např.:'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101'")
    parser.add_argument("name", type=str,                                                                       # 2.argument pro zadání jména CSV souboru
                    help="Napiš jméno CSV souboru i s příponou .csv 'vysledky_ceske_budejovice.csv' ")
    
    
    


   
    args = parser.parse_args()  
    
    
    args = parser.parse_args()
    answer = args.url_adress                    #pojmenování 1.argumentu
    file_name = args.name                       #pojmenování 2.argumentu
    file_name = str(file_name)


    
   
    if parsers_celek(answer,district(a_tag(adress))) == False or parsers_name(file_name) == False:                  #pokud je jeden nebo oba z argumenů špatně,
        print("Chybné zadání")                                                                                       #program vypíše hlášku a ukončí se
        exit()
    else:                                                                                                           #pokud je vše v pořádku, vypíše se print
        new_url = answer
        print("Stahuji data z vybraného URL:", new_url)
        
        
        odpoved = requests.get(new_url)                                                                             # nová adresa od uživatele
        
        if odpoved.status_code != 200:                                                                              # ověří se připojení, pokud je chyba, program se ukončí
            quit()
            
        else:
            soup = bs(odpoved.text, features="html.parser")                                                         
            code = codes(tr_tag(new_url))                                                                            # získání code do tabulky
           
            name_city = list_name(tr_tag(new_url))                                                                  # získání jména měst do tabulky
            
            city_url = link(all_a(all_td(new_url)))                                                                 # získání všech url pro jednotlivá města z okresu
           
            
            print("Ukládám do souboru:", file_name) 

            registr = []                                                                                            # prázdné listy pro data do tabulky
            envelop = []
            valids = []
            quantit = []

            for last_url in city_url:                                                                                  # kontrola všech URL z listu city_url
                odpoved = requests.get(last_url)
                if odpoved.status_code != 200:                                                                        # pokud je chyba program se ukončí
                    quit()
                else:                                                                                                   #pokud je vše v pořádku, pokračuje
                    soup = bs(odpoved.text, features="html.parser")
                    last_url = str(last_url)
                    
                    k = registr.append(registered(last_url))                                                           #získání dat do tabulky a přidání do listů, 
                    l = envelop.append(envelopes(last_url))                                                             #které byly vytvořené na řádce 245-248
                    m = valids.append(valid(last_url))
                    n = quantit.append(quantity(tr_tag(last_url)))

                
            # jeden odkaz pro zjištění názvů politických stran
            for one in city_url:
                o = one[:84]
            p_parties = political_parties(tr_tag(o))
           

           # Hlavička pro DataFrame
            head = ("code", "location", "registered", "envelopes", "valid")
            
           
            # Základní sloupce pro DataFrame
            data = [code, name_city, registr, envelop, valids]  
            # Poté přidáme p_parties, použijeme zip, protože quantit je list obsahující další listy
            data.extend(zip(*quantit))  

            # Sloupce pro DataFrame (připojíme p_parties jako nové sloupce, protože p_parties je tuple)
            columns = list(head) + list(p_parties)

            # Vytvoření DataFrame
            df = pd.DataFrame(list(zip(*data)), columns=columns)


            # Uložení do CSV souboru a poslední print o ukončení
            df.to_csv(file_name, sep="|",index=False, encoding="utf-8", date_format=str)
            print("Ukončuji election scraper.")
           
           # main funkce
            def main():
                if __name__=="__main__":
                    main()


                    