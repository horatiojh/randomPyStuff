# the idea of this script is to input a library and a list of books, then get a return
# value of all the books which are available in that library
# it should also be able, eventually, to, given a list of books and a list of libraries,
# return which library has the most available books

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv
import pandas as pd
import xlsxwriter

# TODO: See if I can parse directly from my account 

# Library books that i'm interested in
books = ['https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95150935/246739648?RECDISP=REC',
'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95203520/171894760?RECDISP=REC',
'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95203524/178142215?RECDISP=REC',
'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95203539/312945068?RECDISP=REC']


# Library that I want to see
selectedLib = "orchard"


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
    print("Getting book at " + url)
    uClient = uReq(url)
    page_html = uClient.read()  # stores the content into a variable
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    tmp = page_soup.find('table')
    # # have to cast to string before passing into regex
    bookTitle = re.search(r"data-title=\"([\w\s]+)\"", str(tmp)).group(1)
    print("Book Title is " + bookTitle)

    statusTable = page_soup.find('table').findAll('tr')
    table = html_stripper(statusTable)

    # we now use regex to find all the library names and availability
    
    libs = re.findall(r"[A-Z][\w\s]* Library|library@[a-z]*", table)
    status = re.findall(r'(Available|Due: [0-9]{2} [A-Za-z]{3} [0-9]{4}),', table)
    output = list(zip(libs, status))

    # test = [v for i, v in enumerate(output) if selectedLib in i]
    def findStatus(lst):
        for item in lst:
            if selectedLib.lower() in item[0].lower():
                # print(item[0], item[1])
                if (item[1] == "Available"):
                    return ("Available")
        return ("Not Available")

    bookStatus = findStatus(output)
    print(bookTitle + ' is ' + bookStatus + ' at ' + selectedLib)

    # TODO: add actual library name instead of user input
    # TODO: if Not Avail, state if it's cos on loan or not even present. if on loan, return earlier loan date 

    return (bookTitle, bookStatus)

    # print(tmp)
    # return

# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95203539/312945068/?RECDISP=REC') #does not work
get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95150935/246739648/?RECDISP=REC') #works
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95203524/178142215/?RECDISP=REC') #dnw
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95203520/171894760/?RECDISP=REC') #dnw
# get_book('https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/XHLD/WPAC/BIBENQ/95210798/312945068?RECDISP=REC') #works




# for i in books:
#     get_book(i)

# TODO: error message if book not found 


# # useful regex 
# # get lib names
# re.findall(r'[A-Z][\w\s]* Library', table)
# # get all statuses 
# re.findall(r'(Available|Due: [0-9]{2} [A-Za-z]{3} [0-9]{4}),', table)
