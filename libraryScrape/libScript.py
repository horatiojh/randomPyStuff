# the idea of this script is to input a library and a list of books, then get a return
# value of all the books which are available in that library
# it should also be able, eventually, to, given a list of books and a list of libraries,
# return which library has the most available books

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd
import xlsxwriter

# TODO: See if I can parse directly from my account 
# TODO: error message if book not found

# write function to try to search book, so that we can always get the URL (is this possible?)


# Library books that i'm interested in
books = ['https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95357198/246739648',
'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95360467/171894760',
'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95365926/178142215',
'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95370061/312945068']


# Library that I want to see
selectedLib = "sengkang"
selectedLibParsed = selectedLib.capitalize()
count = 0

def html_stripper(html):
    # remove all special characters first except @
    x = re.sub('<[^<]+?>', '', str(html))  # gotta coerce to string
    # x = re.sub('\n', ' ', x)
    # this removes all whitespace and makes single space
    # x = re.sub('\s+', ' ', x).strip()
    return(x)

# this function, should, given a url, return the book name and status in a tuple
# for the selected library
def get_book(url):

    # print("Getting book at " + url)
    uClient = uReq(url)
    page_html = uClient.read()  # stores the content into a variable
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    tmp = page_soup.find('table')
    # # have to cast to string before passing into regex
    # bookTitle='a'
    bookTitle = re.search(r"data-title=\"([\w\s\.]+)\"", str(tmp)).group(1)
    # print("Book Title is " + bookTitle)

    statusTable = page_soup.find('table').findAll('tr')
    table = html_stripper(statusTable)

    # we now use regex to find all the library names and availability
    libs = re.findall(r"[A-Z][\w\s]* Library|library@[a-z]*", table)
    # there are 3 statuses: Available, In-transit, or Due: DD Mmm YYYY 
    status = re.findall(r'Available|Due: [0-9]{2} [A-Za-z]{3} [0-9]{4}|In-transit', table)
    output = list(zip(libs, status))
    # print(output)

    # test = [v for i, v in enumerate(output) if selectedLib in i]
    def findStatus(lst):
        global count 
        global selectedLibParsed
        count = 0 
        tmp = ''
        for item in lst:
            if selectedLib.lower() in item[0].lower():
                selectedLibParsed = item[0]
                # print(item[0], item[1])
                if (item[1] == "Available"):
                    count += 1
                else:
    # # TODO: if on loan, return earlier loan date 
                    tmp = item[1]


        if count == 0:
            if tmp == '':
                return("not available at this library")
            return (tmp)
        # print("There is " + str(count) + " copy available for loan at " + selectedLibParsed) if count == 1 else print("There are " + str(count) + " copies available for loan at " + selectedLib) 
        return ("Available")

    bookStatus = findStatus(output)
    # print(bookTitle + ' is ' + bookStatus + ' at ' + selectedLibParsed)
    

    # print(bookTitle, bookStatus, count)
    return (bookTitle, bookStatus, count)

    # testing print statements
    # print(page_soup)
    # print(tmp)
    # print(table)
    # return


# iterate over the books with the above function 
summaryList = []
for i in books:
    summaryList.append(get_book(i))

# print(summaryList)

# OUTPUT TO USER:
availFlag = False # this flag tracks if there are any books available

printListAvail = []
printListUnavail = []
for i in summaryList:
    if i[1] == "Available":
        availFlag = True
        tmpPrint = (str(i[2]) + " copy available for loan.") if i[2] == 1 else (str(i[2]) + " copies available for loan.") 
        printListAvail.append(i[0] + ": " + tmpPrint)
    else: 
        tmpPrint = (i[0] + " is " + i[1])
        printListUnavail.append(tmpPrint)

print("Getting Books:\n")
if availFlag:
    print("The Available books at " + selectedLibParsed + " are:\n")
    for i in printListAvail: 
        print(i)
    print("\n")
else:
    print("None of the books are available at " + selectedLibParsed + " \U0001f97A\n" )
print("Here is the status of the Unavailable Books:\n")
for i in printListUnavail: 
    print(i)

# # useful regex 
# # get lib names
# re.findall(r'[A-Z][\w\s]* Library', table)
# # get all statuses 
# re.findall(r'(Available|Due: [0-9]{2} [A-Za-z]{3} [0-9]{4}),', table)

# test cases 
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95357198/246739648') #works MILKMAN
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95360467/171894760') #works Stories of your life 
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95365926/178142215') #works Do Not Say We Have Nothing
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95370061/312945068') #works Galatea
