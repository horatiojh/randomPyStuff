import pandas as pd
import calendar
from termcolor import colored

########################################## EDIT THIS PART #######################################

csv = '/Users/horatio/Coding/pyScripts/creditCardStatementChecker/resources/1812.csv'
month = 12 # calculates that month's statement, from 16 of prev month to 15 of that month
year = 2022
maxCashback = 30 # monthly max cashback is $30

###################################### DO NOT EDIT THIS PART #######################################

def getStartDate(month):
    if month < 11:
        output = '16/0' + str(month-1) + '/' + str(year)
        return output
    return ('16/' + str(month-1) + '/' + str(year))

def getEndDate(month):
    if month < 10:
        output = '15/0' +str(month) + '/' + str(year)
        return output
    return ('15/' + str(month) + '/' + str(year))

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
data

# remove foreign currency amt, as we don't care about that
del data['Foreign Currency Amount']

# clean data in various columns
data['Date'] = data['Date'].str.replace('\t\t\t','')
data['Date'] = data['Date'].str.lstrip()
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
data['SGD Amount'] = data['SGD Amount'].apply(amtDueStringToInt)

# get cashback amount credited to acc
# idxmax returns the row number of the first occurence of "30CSHBK"
# iloc is then use to get the values iloc[row, column] (zero-indexed)
# we then flip the sign since the cashback shows as a negative balance on the statement

cashbackReceived = -data.iloc[(data['DESCRIPTION'] == "30CASHBACK").idxmax(),2]


# filter by the dates that we want
monthTransactions = data[(data['Date'] >= start) & (data['Date'] <= end)]
monthTransactions

# calculate cashback earned -> this is not just amt due, cos that deducts
# credit. But we get cashback for all money spent! not just amt owed
# also check value against max cashback that we're eligible for
# to get that, we just add all positive transactions from above table
cashbackAmt = monthTransactions.loc[monthTransactions['SGD Amount'] > 0, 'SGD Amount'].sum()

# cashbackAmt = amtDue*0.02 # this is way easier but wont be accurate
cashbackAmt = round(cashbackAmt, 2)
if (cashbackAmt > maxCashback):
    cashbackAmt = maxCashback

# remove first instance of repayment, as it will mess up the amounts
# this sorts by biggest negative amt first, which will be the repayment
# might cause a bug if prev month repayment amt was low tho
tst = monthTransactions.sort_values('SGD Amount').reset_index()
tst = tst.drop(0)

owedAmt = tst["SGD Amount"].sum()
owedAmt = round(owedAmt, 2)

# if amount is arbitrary, check transactions made on 14/15 of the month, as they might have transacted but not
# yet been posted. Item has to be posted by 15th to be in this month's statement
# By this logic, the statement balance should always be <= the amount owed
print("The statement is being calculated for the month of " + calendar.month_name[month], ", using " + csv)
print("The total amount owed is $" + str(owedAmt))
print("The amount being asked for is $" + str(amtDue))
if owedAmt != amtDue:
    print(colored("The statement does not tally", 'red'))
    print("There could be a transaction that wasn't posted in time. The about being asked should be less than that being owed.")
else:
    print("The statement tallies")

print("The cashback amount I should have gotten (assuming 2% on everything) is: $" + str(cashbackAmt))
print("The actual cashback received is: $" + str(cashbackReceived))
if cashbackAmt != cashbackReceived:
    print(colored("The cashback does not tally", 'red'))
    print("The cashback is less by $" + str(round(cashbackAmt-cashbackReceived,2)))
else:
    print("The cashback tallies")


# pd.set_option('display.max_rows',None)
