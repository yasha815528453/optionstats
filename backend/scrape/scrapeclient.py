import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

# Set the User-Agent header to a fake client

class ScrapeClient:
    def __init__(self):

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}



    def get_fed_funds_rate(self):
        url = 'https://www.federalreserve.gov/releases/h15/'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        ele = soup.find_all("td", {"class":"data"})
        return float(ele[4].text)

    def get_sector_industry_country(self, ticker):
        sleep(randint(1,4))
        try:
            url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(ticker, ticker)
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            element = soup.find_all("span", {"class":"Fw(600)"})
            sector = element[1].text
            industry = element[2].text
            content = soup.find_all('p', {"class":"D(ib) W(47.727%) Pend(40px)"})
            country = "empty"

            for tag in content:
                if tag.find_all('br') is not None:
                    if any(char.isdigit() for char in tag.find_all('br')[1].next_sibling):
                        country = tag.find_all('br')[2].next_sibling
                    else:
                        country = tag.find_all('br')[1].next_sibling

            return (sector, industry, country)

        except Exception as e:
            print(e)
            print(ticker)


    def get_category(self, ticker):
        sleep(randint(1,4))
        try:
            url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(ticker, ticker)
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            element = soup.find_all("span", {"class":"Fl(end)"})
            return element[0].text
        except Exception as e:
            print(e)
            print(ticker)
