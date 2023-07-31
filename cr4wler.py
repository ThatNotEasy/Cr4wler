# Author: Pari Malam

import requests
from urllib.parse import urljoin
import time
import pprint
import os
from sys import stdout
from bs4 import BeautifulSoup
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

FY = Fore.YELLOW
FG = Fore.GREEN
FR = Fore.RED
FW = Fore.WHITE
FC = Fore.CYAN

def dirdar():
    if not os.path.exists('Results'):
        os.mkdir('Results')

def crawler():
    os.system('clear' if os.name == 'posix' else 'cls')
    stdout.write("                                                                                            \n")
    stdout.write(""+Fore.LIGHTRED_EX +" ██████╗██████╗ ██╗  ██╗██╗    ██╗██╗     ███████╗██████╗              \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╔════╝██╔══██╗██║  ██║██║    ██║██║     ██╔════╝██╔══██╗             \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝             \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║     ██╔══██╗╚════██║██║███╗██║██║     ██╔══╝  ██╔══██╗             \n")
    stdout.write(""+Fore.LIGHTRED_EX +"╚██████╗██║  ██║     ██║╚███╔███╔╝███████╗███████╗██║  ██║             \n")
    stdout.write(""+Fore.LIGHTRED_EX +" ╚═════╝╚═╝  ╚═╝     ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝             \n")
    stdout.write(""+Fore.YELLOW +"═════════════╦═════════════════════════════════╦══════════════════════════════\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"DESCRIPTION     "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   AUTOMATED WEB SCRAPPING & CRAWLER                "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n\n")
crawler()

while True:
    inputURL = input(f"{Fore.YELLOW}[IP/URL]   : {Fore.GREEN}{Style.RESET_ALL}")
    if not inputURL.startswith(("http://", "https://")):
        inputURL = "https://" + inputURL
    try:
        requests.get(inputURL)
        break
    except requests.RequestException:
        print(f"{Fore.RED}Please provide a valid URL." + Style.RESET_ALL)

resultUrls = {
    inputURL: False
}

session = requests.Session()


def processOneUrl(url):
    try:
        response = session.get(url, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            fullurl = urljoin(url, link['href'])
            if fullurl.startswith(inputURL) and fullurl not in resultUrls:
                resultUrls[fullurl] = False
        resultUrls[url] = True
    except requests.RequestException:
        resultUrls[url] = True


def moreToCrawl():
    for url, crawled in resultUrls.items():
        if not crawled:
            print(Fore.RED + f'[CR4WLING] : {Fore.GREEN}{url}' + Style.RESET_ALL)
            return url
    return False


max_workers = 30

print(f'{Fore.YELLOW}[STARTED]  : {Fore.GREEN}{time.ctime()}{Style.RESET_ALL}' + '\n')

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    while True:
        toCrawl = moreToCrawl()
        if not toCrawl:
            break
        executor.submit(processOneUrl, toCrawl)
        time.sleep(2)

    executor.shutdown(wait=True)

print(f'{Fore.YELLOW}[COMPLETE]  : {time.ctime()}{Style.RESET_ALL}')
pprint.pprint(resultUrls)
