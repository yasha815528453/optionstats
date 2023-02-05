import requests
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep
from backend.tdamodule import tdamethods
from backend.database import methods as DBmethods


headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

def has_number(inp):
    return any(char.isdigit() for char in inp)




with open ("liquidoptions5.csv", 'r') as file:
    data = csv.reader(file)
    for i in data:
        try:
            # non etfs
            if i[4] == 'N':
                
                #summary page
                summary_url = "https://finance.yahoo.com/quote/{}?p={}".format(i[2], i[2]) 
                response = requests.get(summary_url, headers=headers)
                doc = BeautifulSoup(response.content, "html.parser")
                marketCap = doc.find('td', {'data-test':"MARKET_CAP-value"}).text.strip()
                avgVolume = doc.find('td', {'data-test':"AVERAGE_VOLUME_3MONTH-value"}).text.strip()
                print(marketCap)
                sleep(randint(1,5))
                
                
                #profile page
                profile_url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(i[2], i[2])
                response = requests.get(profile_url, headers=headers)
                info = doc.find_all('span', {'class': 'Fw(600)'})
                sector = info[5].text
                industry = info[6].text
                location = doc.find('p', {'class':"D(ib) W(47.727%) Pend(40px)"})
                geo_info = [BeautifulSoup(_, 'html.parser').text.strip() for _ in str(location).split('<br/>')]
                
                #gets country name
                if(has_number(geo_info[2])):  
                    print(geo_info[3])
                    country = geo_info[3]
                else:
                    country = geo_info[3]

                size = tdamethods.optionSize(i[2])
                #give size in tdamethods. refer database for number

                sleep(randint(1,5))
                insertData = (i[2], marketCap, avgVolume, sector, industry, country, size)
                sql = "INSERT INTO stockss (SYMBOLS, marketcap, avgvolume, sector, industry, country, size) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                DBmethods.execute(sql, insertData)
            #etfs
            else:
                summary_url = "https://finance.yahoo.com/quote/{}?p={}".format(i[2], i[2]) # summary page
                response = requests.get(summary_url, headers=headers)
                doc = BeautifulSoup(response.content, "html.parser")
                netasset = doc.find('td', {'data-test':"NET_ASSETS-value"}).text.strip()
                avgVolume = doc.find('td', {'data-test':"AVERAGE_VOLUME_3MONTH-value"}).text.strip()
                sleep(randint(1,5))
                


                profile_url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(i[2], i[2]) #profile url
                response = requests.get(profile_url, headers=headers)
                doc = BeautifulSoup(response.content, "html.parser")
                category = doc.find("span", {'class':"Fl(end)"})
                
                size = tdamethods.optionSize(i[2])
                insertData = (i[2], netasset, avgVolume, category, size)
                sql = "INSERT INTO stockse (SYMBOLS, netasset, avgvolume, category, size) VALUES (%s, %s, %s, %s, %s)" 
                DBmethods.execute(sql, insertData)
        except Exception as e:
            print(e)


