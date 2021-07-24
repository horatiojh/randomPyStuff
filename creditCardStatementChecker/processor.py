import pandas as pd
import xlsxwriter
import calendar
from termcolor import colored

########################################## EDIT THIS PART #######################################

csv = '/Users/horatio/Coding/pyScripts/creditCardStatementChecker/resources/transactions2407.csv'
month = 7 # calculates July's statement, from 16 Jun to 15 July

###################################### DO NOT EDIT THIS PART #######################################

def getStartDate(month):
    if month < 11:
        output = '16/0' +str(month-1) + '/2021'
        return output
    return ('16/' + str(month-1) + '/2021')

def getEndDate(month):
    if month < 10:
        output = '15/0' +str(month) + '/2021'
        return output
    return ('15/' + str(month) + '/2021')

start = getStartDate(month)
end = getEndDate(month)


# skip the first 3 rows as we don't care about the data there
input = pd.read_csv(csv, skiprows=3)

# we want to keep the billed balance, to corroborate later
amtDue = input.loc[input['Date'] == 'BILLED  BALANCE', "Foreign Currency Amount"]
amtDue = amtDue.iloc[0]
amtDue
# have to remove all the stuff and make it an int
# func takes in string and returns int
def amtDueStringToInt(amtDue):
    if 'SGD' in amtDue:
        amtDue = amtDue.replace("SGD ", "")
    amtDue = amtDue.replace(",", "")
    if 'DR' in amtDue:
        output = float(amtDue.replace(" DR", ""))
    else:
        output = -float(amtDue.replace(" CR", ""))
    return output

amtDue = amtDueStringToInt(amtDue)

# remove the last 5 rows as we don't care about that too, it's the summary data
data = input[:-6]

# remove foreign currency amt, as we don't care about that
del data['Foreign Currency Amount']

# clean data in various columns
data['Date'] = data['Date'].str.replace('\t\t\t','')
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
data['SGD Amount'] = data['SGD Amount'].apply(amtDueStringToInt)

# filter by the dates that we want
monthTransactions = data[(data['Date'] >= start) & (data['Date'] <= end)]
monthTransactions

# remove first instance of repayment, as it will mess up the amounts
tst = monthTransactions.sort_values('SGD Amount').reset_index()
tst = tst.drop(0)

owedAmt = tst["SGD Amount"].sum()
owedAmt = round(owedAmt, 2)


# pd.set_option('display.max_rows',None)

print("The statement is being calculated for the month of " + calendar.month_name[month], ", using " + csv)
print("The total amount owed is " + str(owedAmt))
print("The amount being asked for is " + str(amtDue))
if owedAmt != amtDue:
    print(colored("The statement does not tally", 'red'))
else:
    print("The statement tallies")
