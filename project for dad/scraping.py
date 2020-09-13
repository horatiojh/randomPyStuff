from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv


def html_stripper(html):
    x = re.sub('<[^<]+?>', '', str(html)) #gotta coerce to string
    x = re.sub('\n', ' ', x)
    x = re.sub( '\s+', ' ', x).strip() #this removes all whitespace and makes single space
    return(x)


#write a function of this code, that takes in a list of lists, and stores it as an array/data frame
#the urls dont change except for the counter data, so if we can just input counters it would be easier
#then we can manipulate the URL. Think about error handling, especially if the value is not found.


my_url = 'http://www.shareinvestor.com/fundamental/factsheet.html?counter=A17U.SI'
uClient = uReq(my_url) #this grabs the page
page_html = uClient.read() #stores the content into a variable
uClient.close() #closes client

page_soup = soup(page_html, "html.parser")

stockprice = page_soup.findAll("div",{"id":"sic_stockQuote_companyInfo"})
stockprice
first_table = html_stripper(stockprice)

table = page_soup.findAll("table",{"class":"sic_table sic_tableBigCell"})
cleaned_table = html_stripper(table)
second_table = cleaned_table.rpartition('Par Value')[0]
#this splits the string and returns the substring before 'Par Value'
# [1] gives 'Par Value' and [2] gives the substring after 'Par Value'

raw_data = first_table + second_table #merge data so only need to run function once

#can change the below list to manipulate what variables we want to pull (but make sure the data is there in the stuff we pulled!)
data_wanted = ['Last (SGD)', 'Change:', 'High', 'Low', 'Change (%):', 'Open',
               'Yesterday\'s Close', 'Buy Price', 'Sell Price', 'Buy Volume (\'000)',
               'Sell Volume (\'000)', 'Cumulative Volume (\'000)', 'Cumulative Value',
               'EPS (SGD)', 'Trailing EPS (SGD)', 'NAV (SGD)', 'PE', 'Dividend (SGD)',
               'Trailing PE', 'Price / NAV', 'Dividend Yield (%)', 'hello']

def get_data(lst, string):
    x = [None] * (len(lst)-1) #initialise empty list
    for i in range(len(lst)-1):
        y = string.partition(lst[i])[2].partition(lst[i+1])[0] #gets the value wanted
        y = re.sub(':', '', str(y)).strip()
        y = re.sub('^[\w]? ', '', str(y))
        y = y.partition(' ')[0]
        x[i] = y
        print(x[i])
    return(x)

data = get_data(data_wanted, raw_data)

#1 column is data wanted, another column is data


test2 = list(zip(data_wanted,data))
test2
zipped_list = test2[:]

with open("stock.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(zipped_list)



'''
after this just combine the data and the indicators, and export to CSV.
Then think about how to make it happen for multiple stocks.

takes only the table without price movements, but has notes.
valuestable = page_soup.findAll("div",{"id":"sic_factsheet_fundamental"})
moredata = html_stripper(valuestable)
'''
