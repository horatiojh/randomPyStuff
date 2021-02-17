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

# new approach: we login to an account and try to get the books from the bookmarked page,
# which will circumvent the dynamic URL issue

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


def getDataFromLink(driver, lnk):
    driver.get(lnk)
    time.sleep(1)
    # get the title of the book
    title = driver.find_element_by_xpath('//h5[@class="card-title fullTitleh5"]/span').get_attribute('innerHTML')
    print('Retrieving info for book: ' + title)
    output = driver.find_element_by_xpath('//a[@role="button"][@data-target="#holdingsDlg"]')
    driver.execute_script("arguments[0].click();", output)
    time.sleep(2)
    # tbl = driver.find_element_by_xpath('//table[@class="table table-stacked"]')
    tbl = driver.find_element_by_xpath('//table').get_attribute('outerHTML')
    # print(tbl)
    df = pd.read_html(tbl)[0]
    # print(df)
    return (title,df)


# this function takes in 2 arguments,
# the first is a dictionary where the key is the book title
# and the value is a pandas dataframe comprising the complete statuses.
# the second argument is the library you're searching for
# it returns a list of triples, with the book title, book status, and number of
# available copies

def filterBookInfoByLib(dict, lib):
    outputList = []
    for key in dict:
        title = key
        df = dict.get(key)
        filteredDf = df[df['Library'].str.contains(lib.capitalize())][["Item Status"]].values.tolist()
        # flatten the list of lists and add it to the lst
        flatList = [item for sublist in filteredDf for item in sublist]
        sorted(flatList)
        if len(flatList) == 0:
            triple = (title, "not available at this library", 0)
            outputList.append(triple)
        else:
            count = flatList.count("Available")
            if count == 0:
                triple = (title, flatList[0], 0)
                outputList.append(triple)
            else:
                triple = (title, "Available", count)
                outputList.append(triple)
    return outputList


# this function takes in the list of triples and prints nice stuff for the user to see

def userOutputSingleLib(tripList, lib):
    availFlag = False # this flag tracks if there are any books available
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


    print("Getting Books:\n")
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
    return

################################################################################################################################
############################################# DO NOT EDIT THE PART ABOVE #######################################################

# Only edit the selected library, as well as your user info in the other document

selectedLib = 'bishan' # EDIT THIS
rawInfo = scrapeAllBookInfo()
filteredInfoSingleLib = filterBookInfoByLib(rawInfo, selectedLib)
userOutputSingleLib(filteredInfoSingleLib, selectedLib)
