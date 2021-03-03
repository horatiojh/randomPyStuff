# the idea of this script is to input a library and a list of books, then get a return
# value of all the books which are available in that library
# it should also be able, eventually, to, given a list of books and a list of libraries,
# return which library has the most available books

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from termcolor import colored
import sys
import os
import selenium
from selenium import webdriver
import time
import pandas as pd
import userInfo

# TODO: cache output (maybe store the dict in a separate text file) so that subsequent runs will be fast 
# if the user decides to change parameters

# TODO: make retrieval faster! Don't use Selenium, use a non-GUI scrape instead?

# new approach: we login to an account and try to get the books from the bookmarked page,
# which will circumvent the dynamic URL issue

def getDataFromLink(driver, lnk):
    driver.get(lnk)
    time.sleep(1)
    # get the title of the book
    title = driver.find_element_by_xpath('//h5[@class="card-title fullTitleh5"]/span').get_attribute('innerHTML')
    print('Retrieving info for book: ' + title)
    output = driver.find_element_by_xpath('//a[@role="button"][@data-target="#holdingsDlg"]')
    driver.execute_script("arguments[0].click();", output)
    time.sleep(2.5)
    # tbl = driver.find_element_by_xpath('//table[@class="table table-stacked"]')
    tbl = driver.find_element_by_xpath('//table').get_attribute('outerHTML')
    # print(tbl)
    df = pd.read_html(tbl)[0]
    # print(df)
    return (title,df)

# this function takes in the library of choice as an argument,
# and returns a dictionary of keys and values,
# where the key is a string consisting the book title,
# and the value is a list of statuses

def scrapeAllBookInfo():
    driver = webdriver.Chrome()
    driver.get('https://cassamv2.nlb.gov.sg/cas/login')

    # begin by importing the username and password from a separate file. I do this so I don't have to keep changing this variable when I push my code changes

    # select and fill the username
    userIdBox = driver.find_element_by_id('username')
    userIdBox.send_keys(userInfo.username)

    # select and fill the password
    passwordBox = driver.find_element_by_id('password')
    passwordBox.send_keys(userInfo.password)

    loginButton = driver.find_element_by_name('submit')
    loginButton.click()

    # navigate to the bookmarks page
    driver.get('https://www.nlb.gov.sg/mylibrary/Bookmarks')

    # get the links and filter/clean them
    output = driver.find_elements_by_xpath('//a[@class="item-title-value nowrap-fade text-muted"]')

    links = []
    for item in output:
        href = item.get_attribute('href')
        # we need to append the 'SETLVL=1' if not already set
        if ("SETLVL" not in href):
                href = re.sub('BRN', 'SETLVL=1&BRN', href)
        links.append(href)

    # print(links)

    outputDict = {}
    # for each link, we need to query the page, click on availability, get the loan info and save it to a list of dataframes
    for link in links:
        tmp = getDataFromLink(driver, link)
        if tmp[0] in outputDict:
            vals = outputDict.get(tmp[0])
            newVals = pd.concat([tmp[1], vals])
            outputDict[tmp[0]] = newVals
        else:
            outputDict[tmp[0]] = tmp[1]
    driver.close()
    return(outputDict)


# this function takes in 2 arguments,
# the first is a dictionary where the key is the book title
# and the value is a pandas dataframe comprising the complete statuses.
# the second argument is the library you're searching for
# it returns a dict where the key is the library name 
# and the value is a list of triples of the book title, status, and no. of available copies

def filterBookInfoByLib(dict, libList):
    output = {}
    for lib in libList:
        tmpList = []
        for key in dict:
            title = key
            df = dict.get(key)
            df["Library"] = df["Library"].str.lower()
            filteredDf = df[df['Library'].str.contains(lib.lower())][["Item Status"]].values.tolist()
            # flatten the list of lists and add it to the lst
            flatList = [item for sublist in filteredDf for item in sublist]
            sorted(flatList)
            if len(flatList) == 0:
                triple = (title, "not available at this library", 0)
                tmpList.append(triple)
            else:
                count = flatList.count("Available")
                if count == 0:
                    triple = (title, flatList[0], 0)
                    tmpList.append(triple)
                else:
                    triple = (title, "Available", count)
                    tmpList.append(triple)
        output[lib] = tmpList
    return output


# this function takes in a dict where the keys are the library name 
# and the values are the list of triples and prints nice stuff for the user to see
def userOutputSelectedLibs(tripListDict):
    availFlag = False # this flag tracks if there are any books available
    for key in tripListDict:
        lib = key
        tripList = tripListDict[key]
        printListAvail = []
        printListUnavail = []
        lib = lib.capitalize()
        for i in tripList:
            if i[1] == "Available":
                availFlag = True
                tmpPrint = (str(i[2]) + " copy available for loan.") if i[2] == 1 else (str(i[2]) + " copies available for loan.")
                printListAvail.append(i[0] + ": " + tmpPrint)
            else:
                tmpPrint = (i[0] + " is " + i[1])
                printListUnavail.append(tmpPrint)


        print("Getting Books available at " + lib + ":\n")
        if availFlag:
            tmp = ("The Available books at " + lib + " are:\n")
            print(colored(tmp, 'red'))
            for i in printListAvail:
                print(i)
            print("\n")
        else:
            print("None of the books are available at " + lib + " \U0001f97A\n" )
        tmp = ("Here is the status of the Unavailable Books:\n")
        print(colored(tmp, 'red'))
        for i in printListUnavail:
            print(i)
        print("\n")
    return


# this function takes in the dict from the first function
# it returns all the libraries where the books are available to a dict,
# where the keys are the library, and the values are the books avail at that lib
# we also need to keep a running counter so that we can sort by the library with the most books later

def getAllLibInfo(dict):
    output = {}
    for book in dict:
        df = dict.get(book)
        filteredDf = df[df['Item Status'].str.contains("Available")][["Library"]].values.tolist()
        flatList = [item for sublist in filteredDf for item in sublist]
        # remove duplicate entries
        flatList = list(set(flatList))
        # for library in list of libraries
        for lib in flatList:
            if lib in output:
                currVal = output[lib]
                currVal[1].append(book)
                newVal = (currVal[0] + 1, currVal[1])
                output[lib] = newVal
            else:
                output[lib] = (1, [book])
    return output

# this function takes in 2 arguments: 
# a dictionary where the keys are the library, 
# and the values are the number of books and title of books avail at that lib 
# the second argument is the number of books that the libraries should minimally have
# 
# it prints the info to the user 

def printAllLibInfo(allLibInfoDict, numPrint):
    toPrint = dict(sorted(allLibInfoDict.items(), key=lambda item: item[1], reverse=True))
    toPrint = { k:v for k, v in toPrint.items() if v[0] >= numPrint }
    # if dict is empty just let user know and end
    if (not allLibInfoDict):
        print(colored("There are no books available at any library... \U0001f97A\n", 'red'))
        return
    for lib in toPrint:
        libVal = lib.title()
        val = toPrint[lib]
        count = val[0]
        books = val[1]
        print(colored("There are " + str(count) + " books available at " + libVal + ":\n", 'green'))
        for book in books:
            print(book)
        print("\n")
    return

################################################################################################################################
############################################# DO NOT EDIT THE PART ABOVE #######################################################

# Only edit the selected library, as well as your user info in the other document

# this is a list, so just add the libraries you wanna find in the [] brackets
# each library name should be surrounded by inverted commas, and each name should be separated by a comma
selectedLib = ['orchard', 'bishan', 'sengkang'] # <------- EDIT THIS

rawInfo = scrapeAllBookInfo()
filteredInfoSelectedLibs = filterBookInfoByLib(rawInfo, selectedLib)
userOutputSelectedLibs(filteredInfoSelectedLibs)

# For all library info
allLibInfo = getAllLibInfo(rawInfo)
printAllLibInfo(allLibInfo, 3)
