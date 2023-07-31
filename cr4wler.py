# Author: Pari Malam

import argparse
import threading
import random
import os
import time
import sys
from urllib.request import urlopen, Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
from html.parser import HTMLParser
from urllib.parse import urljoin
from sys import stdout
from colorama import Fore, Style

FY = Fore.YELLOW
FG = Fore.GREEN
FR = Fore.RED
FW = Fore.WHITE
FC = Fore.CYAN

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

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


sys.setrecursionlimit(1000)

class LinkHTMLParser(HTMLParser):
    A_TAG = "a"
    HREF_ATTRIBUTE = "href"

    def __init__(self):
        self.links = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == self.A_TAG:
            for (key, value) in attrs:
                if key == self.HREF_ATTRIBUTE:
                    self.links.append(value)

    def handle_endtag(self, tag):
        pass


class CrawlerThread(threading.Thread):
    binarySemaphore = threading.Semaphore(1)

    def __init__(self, url, crawlDepth, output_file):
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        self.url = url
        self.crawlDepth = crawlDepth
        self.threadId = hash(self)
        self.request_interval = 2
        self.user_agents = self.load_user_agents()
        self.output_file = output_file
        super().__init__()

    def load_user_agents(self):
        with open("lib/ua.txt", "r") as file:
            return [line.strip() for line in file.readlines()]

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def is_excluded_domain(self, url):
        excluded_domains = ["whatsapp.com", "twitter.com", "facebook.com", "youtube.com", "linkedin.com", "instagram.com"]
        for domain in excluded_domains:
            if domain in url:
                return True
        return False

    def save_to_file(self, url):
        dirdar()
        with open(self.output_file, "a") as file:
            file.write(url + "\n")

    def run(self):
        user_agent = self.get_random_user_agent()
        headers = {'User-Agent': user_agent}
        req = Request(self.url, headers=headers)
        try:
            opener = build_opener(HTTPRedirectHandler())
            socket = opener.open(req, timeout=10)
            urlMarkUp = socket.read().decode('utf-8')
            linkHTMLParser = LinkHTMLParser()
            linkHTMLParser.feed(urlMarkUp)
            CrawlerThread.binarySemaphore.acquire()
            print(f"{FY}[CR4WLER] - {FG}Thread: {FC}#{self.threadId} {FR}| {FW}Reading from {FC}{self.url}{Style.RESET_ALL}")
            print(f"{FY}[CR4WLER] - {FG}Thread: {FC}#{self.threadId} {FR}| {FW}Crawl Depth = {FC}{self.crawlDepth}{Style.RESET_ALL}")
            print(f"{FY}[CR4WLER] - {FG}Thread: {FC}#{self.threadId} {FR}| {FW}Retrieved the following links...{Style.RESET_ALL}")
            urls = []
            for link in linkHTMLParser.links:
                link = urljoin(self.url, link)
                if not self.is_excluded_domain(link):
                    urls.append(link)
                    print(f"{FY}[CR4WLER] - {FG}Thread: {FC}#{self.threadId} {FR}| {FG}[Found]: {FC}{link}{Style.RESET_ALL}")
                    self.save_to_file(link)
            print("")
            CrawlerThread.binarySemaphore.release()
            for url in urls:
                if self.crawlDepth > 1:
                    time.sleep(self.request_interval)
                    CrawlerThread(url, self.crawlDepth - 1, self.output_file).start()
        except HTTPError as e:
            if e.code == 302:
                redirected_url = e.headers.get("Location")
                if redirected_url:
                    CrawlerThread(redirected_url, self.crawlDepth, self.output_file).start()
            else:
                print(f"{FY}[CR4WLER] - {FG}Thread: {FC}#{self.threadId} {FR}| [Failed] - {FC}{self.url}{FR}: {Style.RESET_ALL}")
        except Exception as e:
            print(f"{FY}[CR4WLER] - {FG}Thread: {FC}#{self.threadId} {FR}| [Error] - {FC}{self.url}{FR}: {e}{Style.RESET_ALL}")

def get_input_from_user():
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("-u", "--url", required=True, help="URL to crawl")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads (default: 1)")
    parser.add_argument("-o", "--output", default="Results/Cr4wler.txt", help="Output filename")
    args = parser.parse_args()

    if args.output == "Results/Cr4wler.txt":
        args.output = os.path.join("Results", "Cr4wler.txt")

    return args

if __name__ == "__main__":
    args = get_input_from_user()
    output_file = args.output
    url = args.url
    num_threads = args.threads

    for _ in range(num_threads):
        CrawlerThread(url, crawlDepth=10, output_file=output_file).start()
