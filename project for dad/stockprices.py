from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd
import xlsxwriter

######################################################### EDIT THIS #########################################################

# change this to the directory that the excel file should be saved to 
outputDir = 'stocks.xlsx'

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

######################################################### DO NOT EDIT THIS #########################################################
def html_stripper(html):
    x = re.sub('<[^<]+?>', '', str(html)) #gotta coerce to string
    x = re.sub('\n', ' ', x)
    x = re.sub( '\s+', ' ', x).strip() #this removes all whitespace and makes single space
    return(x)

def get_price(url):
    print("Fetching value for " + url)
    uClient = uReq(url)
    page_html = uClient.read() #stores the content into a variable
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    page_soup

    stockprice = page_soup.findAll("div",{"id":"sic_stockQuote_companyInfo"})
    table = html_stripper(stockprice)
    # print(table)

    # use this regex if you want the actual name
    name = re.search(r'\[ .*?(?= [A-Z]{2}| Quotes)', table)
    name = name.group(0)
    name = name.partition(" ")[2]
    name = re.sub('&amp;', '&', name)

    # # use this regex if you want the counter name 
    # name = re.search(r'(?<=counter=).*$', url)
    # name = name.group(0)

    # print(name)
    price = table.partition(': ')[2].partition(' Change:')[0]
    price = re.sub(',', '', price) #remove commas from the value if it's more than $1000

    return(name, price)


new_list = []
for i in stock_urls:
    new_list.append(get_price(i))

names, price = zip(*new_list)
names  = list(names)
price = list(price)

price = list(map(float, price))

df = pd.DataFrame({'Names': names,'Price':price})

writer = pd.ExcelWriter(outputDir, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()