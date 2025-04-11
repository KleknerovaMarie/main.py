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

def request_check(url: str) -> bs:
    """"
    Odesílá GET požadavek na zadanou URL a vrací objekt BeautifulSoup pro parsování HTML.
    Parametr je url(str): url stránky.
    Návratová hodnota:
        quit pokud dojde k chybě
        soup(bs) pokud je vše v pořádku
    Příklad:
        request_check('https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
    """
    odpoved = requests.get(url)
    if odpoved.status_code != 200:
        print(f'Chyba při připojení k URL: {url}')
        return exit()
    else:
        soup = bs(odpoved.text, features='html.parser')  
        return soup
    

def district(soup: bs) -> list:
    """"
    District získá seznam všech URL jednotilivých okresů.
    Parametr je soup(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check.
    Návratová hodnota:
        first_links(list) seznam URL adres 
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss')
        sample = district(soup)
        print[sample]
            ['https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&amp;xkraj=2&amp;xnumnuts=2101', 
                https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&amp;xkraj=2&amp;xnumnuts=2104']
    """
    a_tags = []
    first_links = []
    vsechny = soup.find_all("a")
    for kus in vsechny:
        kus_append = a_tags.append(kus.get("href"))
    for part in a_tags:
        part = str(part)
        if part[:4] == 'ps32' or part[:5] == 'ps36?':
            url_append = first_links.append('https://www.volby.cz/pls/ps2017nss/' + part)
        else:    
            continue
    return first_links


def list_name(soup: bs) -> list:
    """
    List_name získává jména všech měst.
    Parametr je soup(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check. 
    Návratová hodnota:
        city(list) seznam všech jmen měst v okrese
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100')
        sample = list_name(soup)
        print(sample)
            ['Praha 1', 'Praha 10', 'Praha 11']
    """
    city = []
    all_td = soup.find_all('td', {'class' :'overflow_name'})
    all_headers = soup.find_all('td',{'headers': 's3'})
    if all_td:
        for okres in all_td:
            jmena_okresu = okres.get_text(strip=True)
            if jmena_okresu not in ('název', 'VýběrPM', 'Výběrokrsku' '-') and jmena_okresu != '':
                city_append = city.append(jmena_okresu)
            else:
                continue
    else:
        for headers in all_headers:
            cizina_nazvy = headers.get_text(strip=True) 
            city_appends = city.append(cizina_nazvy)
    return city 


def link(soup: bs) -> list:
    """
    Link získává URL všech měst.
    Parametr je soup(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check.
    Návratová hodnota:
        links(list) seznam všech URL k jednotlivým městův v okrese.
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100')
        sample = link(soup)
        print(sample)
            ['https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1&xobec=500054&xvyber=1100',     
                'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1&xobec=500224&xvyber=1100']
    """
    links = []
    every_td = soup.find_all('td', {'class': 'cislo'})
    for td in every_td:
        a_tag = td.find('a')
        if a_tag:
            clean_link = a_tag['href'].replace('amp;', '')
            final_link = 'https://www.volby.cz/pls/ps2017nss/' + clean_link
            append_links = links.append(final_link)
    return links


def cleaner(list_of_numbers: list) -> str:
    """
    Cleaner odstraňuje pevné mezery.
    Parametr je list_of_numbers(list): list obsahující čísla, která mohou obsahovat pevné mezery.
    Návratová hodnota:
        clean_list(str) string obsahující upravená čísla
    Příklad:
        cleaner(['12\xa0323', '2\xa0123'])
        print(clean_list)
            ['12323', '2123']
    """
    list_of_numbers = str(list_of_numbers)
    clean_list = list_of_numbers.replace("\xa0", "")
    return clean_list 


def codes(soup: bs) -> list:
    """
    Codes hledá všechny kódy jednotlivých měst v okrese.
    Parametr je soub(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check.
    Návratová hodnota:
        code(list) list obsahující kódy jednotlivých měst
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100')
        sample = codes(soup)
        print(sample)
            ['500054', '500224', '547034']
    """
    code = []
    all_td = soup.find_all('td', class_ = 'cislo')  
    for td in all_td:
        cisla_mest = td.get_text()
        cisla_mest = str(cisla_mest)
        if cisla_mest.isalpha():                      
            continue
        else:
           code_append = code.append(cisla_mest)
    return code


def searching_headers(soup: bs, headers: str) -> str:
    """
    Searching_headers získává počety ze zadaných headers z URL a použije funkci cleaner pro úpravu čísla.
    Parametr je soup(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check
                headers(str): string u td prvku 
    Návratová hodnota:
        clean_searching(str) string obsahující jedno číslo, upravené pomocí funkce cleaner
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1&xobec=500054&xvyber=1100')
        sample = registered(soup, 'sa2')
        print(sample)
            ['21556']
    """
    searching = soup.find('td', {'class': 'cislo', 'headers': headers}).text
    clean_searching = cleaner(searching)
    return clean_searching


def political_parties(soup: bs) -> list:
    """
    Political_parties získává jména politických stran z URL.
    Parametr je soup(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check.
    Návratová hodnota:
        politics_parties(list) list obsahující seznam politických hlasů 
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1&xobec=500054&xvyber=1100')
        sample = political_parties(soup)
        print(sample)
            ['Občanská demokratická strana', 'Řád národa - Vlastenecká unie', 'CESTA ODPOVĚDNÉ SPOLEČNOSTI']
    """
    politics_parties = []
    every_td_overflow = soup.find_all('td', class_='overflow_name')
    for one_td in every_td_overflow:
        parties = one_td.get_text()
        if parties in ('název', 'Platné hlasy', '-') or parties.isdigit():
            continue
        elif parties in politics_parties:
            continue
        else:
            parties_append = politics_parties.append(parties)
    return politics_parties


def quantity(soup: bs) -> list:
    """
    Quantity získává počet hlasů u jednotlivých politických stran z URL a nakonec použije funkci cleaner
      pro odstranění pevných mezer a vybere každý třetí údaj.
    Parametr je soup(bs): BeautifulSoup, který obsahuje obsah HTML stránky, z funkce request_check.
    Návratová hodnota:
        clean_votes(list) list obsahující počet hlasů jednotlivých politických stran s odstraněnými pevnými mezerami
    Příklad:
        soup = request_check('https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1&xobec=500054&xvyber=1100')
        sample = quantity(soup)
        print(sample)
            ['2770', '9', '13', '657', '12','1']
    """
    votes = []
    clean_votes = []
    tr_votes = soup.find_all('tr')
    for data in tr_votes[3:]:
        vote = data.find_all('td', class_= 'cislo')
        for td in vote:
            votes_append = votes.append(td.get_text(strip=True))
    better_votes = votes[1::3]
    for one_vote in better_votes:
        cleaned_vote = cleaner(one_vote)
        clean_append = clean_votes.append(cleaned_vote)
    return clean_votes


parser.add_argument("url_adress", type=str,                                          # 1.argument pro zadání URL
            help="Napiš url odkaz např.:'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101'")
parser.add_argument("name", type=str,                                                # 2.argument pro zadání jména CSV souboru
            help="Napiš jméno CSV souboru i s příponou .csv 'vysledky_ceske_budejovice.csv' ")
    
args = parser.parse_args()  
answer = args.url_adress                    #pojmenování 1.argumentu
file_name = args.name                       #pojmenování 2.argumentu
file_name = str(file_name)
           

def main(): 
    """
    Hlavní funkce programu, která provádí následující kroky:
    - Načte argumenty z příkazové řádky
    - Zkontroluje platnost URL adresy a názvu CSV souboru, pokud je jeden nebo oba z argumenů špatně 
        program vypíše hlášku a ukončí se. Pokud je vše v pořádku, kód pokračuje.
    - Stáhne data z volebního serveru pro daný okres a pro jednotlivá města
    - Zpracuje a uloží získaná data do CSV souboru, jako jméno souboru se použije 2.argument file_name
    Parametry:
        žádné
    Návratová hodnota:
        žádné (funkce nic nevrací)
    Příklad použití:
        Pokud je skript spuštěn příkazovou řádkou, funkce `main()` se automaticky spustí.
    """  

    adress = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

         
    if answer not in district((request_check(adress))) or not file_name.endswith('.csv') :                  
        print("Chybné zadání")                                                                                       
        exit()
    else:                                                                                                           
        new_url = answer
        print("Stahuji data z vybraného URL:", new_url)
        soup = request_check(new_url)
        code = codes(soup)
        name_city = list_name(soup)
        city_url = link(soup)
        print("Ukládám do souboru:", file_name) 

        registr = []                                                                                            
        envelop = []
        valids = []
        quantit = []
   
        for last_url in city_url:                                                                                  
            soup = request_check(last_url)
            registr_append = registr.append(searching_headers(soup, 'sa2'))                                                            
            envelop_append = envelop.append(searching_headers(soup, 'sa3'))                                                             
            valid_append = valids.append(searching_headers(soup, 'sa6'))
            quantit_append = quantit.append(quantity(soup))   
            p_parties = political_parties(soup)
                      
        head = ("code", "location", "registered", "envelopes", "valid")
        data = [code, name_city, registr, envelop, valids]  
        data.extend(zip(*quantit))  
        columns = list(head) + list(p_parties)
        df = pd.DataFrame(list(zip(*data)), columns=columns)   


    
        df.to_csv(file_name, sep="|",index=False, encoding="utf-8", date_format=str)
        print("Ukončuji election scraper.")

if __name__== "__main__":    
    main()
   

                    