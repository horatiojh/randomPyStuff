from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd
import xlsxwriter

def html_stripper(html):
    x = re.sub('<[^<]+?>', '', str(html)) #gotta coerce to string
    x = re.sub('\n', ' ', x)
    x = re.sub( '\s+', ' ', x).strip() #this removes all whitespace and makes single space
    return(x)

def get_price(url):
    uClient = uReq(url)
    page_html = uClient.read() #stores the content into a variable
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    stockprice = page_soup.findAll("div",{"id":"sic_stockQuote_companyInfo"})
    table = html_stripper(stockprice)
    name = re.search(r'(\[ ).*?(?=\s[A-Z]{2})', table)
    name = name.group(0)
    name = name.partition(" ")[2]
    price = table.partition(': ')[2].partition(' Change:')[0]

    return(name, price)


stock_urls = ['http://www.shareinvestor.com/fundamental/factsheet.html?counter=A17U.SI', #Ascendas REIT
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=C31.SI', #Capitaland
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=RW0U.SI', #MapleTree NAC
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=M44U.SI', #MapleTree Log
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=H78.SI', #HongKongLand USD
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=A68U.SI', #Ascott REIT
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=BUOU.SI', #Frasers L&I
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=BTOU.SI', #Manulife REIT
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=M62.SI', #CIMBASEAN40
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=G1K.SI', #LYXOR Asia
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=D05.SI', #DBS
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=C38U.SI', #Capitamall Trust
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=AW9U.SI', #First REIT
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=S58.SI', #SATS
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=Y92.SI', #ThaiBev
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=ME8U.SI', #Mapletree Ind
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=J69U.SI', #Frasers Cpt Tr
              'http://www.shareinvestor.com/fundamental/factsheet.html?counter=OV8.SI'] #Sheng Shiong

new_list = []
for i in stock_urls:
    new_list.append(get_price(i))

names, price = zip(*new_list)
names  = list(names)
price = list(price)
price = list(map(float, price))


df = pd.DataFrame({'Names': names,'Price':price})

writer = pd.ExcelWriter('Stockprice.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()



'''
zipped_list = new_list[:]

with open("stockprices.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(zipped_list)
'''
