import re
import time
from datetime import datetime, timedelta
import requests
import requests_cache
from bs4 import BeautifulSoup
from urllib.request import quote

# setup (token and stuff)
scriptName = "dpcScheduleCompiler (horatiohotness@gmail.com)"
headers = {'User-Agent': scriptName,'Accept-Encoding': 'gzip'}
requests_cache.install_cache(cache_name='scheduleCache', backend='sqlite', expire_after=6000)

def generate_pages(division, regionList, season):
	pages = []
	season = str(season)
	for region in regionList:
		if division == 1:
			tmp = 'Dota_Pro_Circuit/2021-22/' + season + '/' + region + '/Division_I'
			pages.append(tmp)
		else: 
			tmp = 'Dota_Pro_Circuit/2021-22/' + season + '/' + region + '/Division_II'
			pages.append(tmp)
	return pages

def html_stripper(html):
	x = re.sub('<[^<]+?>', '', str(html)) #gotta coerce to string
	x = re.sub('\n', ' ', x)
	x = re.sub( '\s+', ' ', x).strip() #this removes all whitespace and makes single space
	return(x)

# takes in soup object representing the raw scrape of a week's schedule, returns a list of strings where each string is a match
# sample output: 'December 1, 2021 - 16:00: TNC v T1 (SEA/Div1)'
def getScheduleFromBSObject(soupObj, region, div):

	# get the week it is
	week = re.search(r'Week [0-9]', str(soupObj)).group(0)

	# sort the teams out
	tmp = soupObj.findAll("div", {"class":"brkts-matchlist-cell brkts-matchlist-opponent brkts-opponent-hover"})
	teamRaw = html_stripper(tmp)
	# print(teamRaw)
	teams = teamRaw.replace('[', '').replace(']', '').replace(' ', '').split(',')
	# edit Alliance since they're saved as [A]
	if (region == 'EU' and 'A' in teams):
		teams = [team.replace('A', 'Alliance') for team in teams]

	si = iter(teams)
	matchList = [c+' v '+ next(si, '') + ' (' + region + '/' + div + ')' for c in si]

	# sort the dates out
	dateList = re.findall(r'[A-Z][a-z]* [0-9][0-9]?, [0-9]{4} - [0-9]{2}:[0-9]{2}', str(soupObj))

	# convert timezone if necessary
	updatedDateList = []
	for date in dateList:
		updatedDateList.append(convertDateTime(date, region))
		# print(date)

	# return list(zip(dateList, matchList))
	outputList = [': '.join(z) for z in zip(updatedDateList, matchList)]

	# return the week and the schedule
	# print(week)
	# print(outputList[0])
	return (week, outputList)


# generate a map of string lists, with each week as the key and the map as its value

def createCompleteScheduleForAUrl(inputUrl, season):
	regString = '/' + str(season) + '/(.*)/Di'
	print("Getting schedule from the following URL: " + inputUrl)
	region = re.search(regString, inputUrl).group(1)
	region = convertRegion(region)
	print('Region: ' + region)
	div = re.search(r'Division.*', inputUrl).group(0)
	div = convertDiv(div)
	print('Division: ' + div + "\n")

	output = {}
	soup,url,cached = parse(inputUrl)
	# print(soup)
	schedule = soup.findAll("div",{"class":"brkts-matchlist brkts-matchlist-collapsible"})
	# print(schedule)
	for week in schedule:
		weeklySchedule = getScheduleFromBSObject(week, region, div)
		output[weeklySchedule[0]] = weeklySchedule[1]

	return output, cached

# now we do it for all regions, then we combine the maps to get one list for each week
def createCompleteSchedule(urlList, season):
	output = {}

	# collect individual schedules
	for url in urlList:
		tmp, isCached = createCompleteScheduleForAUrl(url, season)

		# add values to dict
		for week in tmp:
			if week in output:
				currVals = output[week] #list
				output[week] = currVals + tmp[week]
			else:
				output[week] = tmp[week]
		
		# set rate limiting to abide by API regulations (30 sec per parse call) if response was not from cache
		if not isCached:
			print("Value not previously cached, sleeping for 30s to abide by rate limiting...")
			time.sleep(30)

	# sort the lists
	for week in output:
		output[week].sort()
		# format the date 
		tmp = output[week]
		newList = []
		for item in tmp:
			newString = convertDateTimeBackToNiceFormat(item)
			newList.append(newString)  
		output[week] = newList

	return output

def getWeeklySchedule(map, wkNumber, teams):
	week = "Week " + str(wkNumber)
	output = map[week]
	# print("DPC Schedule: " + week)
	
	# if teams is empty means we want all matches
	if not teams:
		# for item in output:
			# print(item)
		return output
	
	# else match against the list provided
	else:
		filteredList = []
		date = ""
		for item in output:
			if any(team in item for team in teams):
				filteredList.append(item)
				tmp = ""
				if (item[:2] != date):
					# print() # create newline so dates are split
					date = item[:2]
				# print(item)
		return filteredList

def printScheduleToTerminal(scheduleList, week, shouldSort):
	week = "Week " + str(week)
	print("DPC Schedule: " + week)
	if shouldSort:
		# sort by Day, then by Time ie. "Mon 10 Jan 13:00: ..." will sort by '10' then '13:00'
		# easiest way to do it without having to reformat strings back to dates, but will cause problems if games over 2 months are scheduled
		# TODO: format/sort by date
		scheduleList.sort(key=lambda x: (x.split(' ')[1], x.split(' ')[3]))
	date = ""
	for item in scheduleList:
		if (item[:2] != date):
			print() # create newline so dates are split
			date = item[:2]
		print(item)



def convertDateTime(dateString, region):
	timeToAdd = calculateRegionTimeDiff(region)
	format = '%B %d, %Y - %H:%M'
	tmp = datetime.strptime(dateString, format)
	newTime = tmp + timedelta(hours=timeToAdd)
	return newTime.strftime('%Y/%m/%d %H:%M')

def convertDateTimeBackToNiceFormat(dateString):
	tmp = str.split(dateString, ": ")
	date = tmp[0]
	game = tmp[1]
	format = ('%Y/%m/%d %H:%M')
	date = datetime.strptime(date, format)
	newDate = date.strftime('%a %d %b %H:%M')
	return newDate + ": " + game

def calculateRegionTimeDiff(region):
	if region == "SEA":
		return 8
	if region == "CN":
		return 8
	if region == "EU":
		return 8
	if region == "CIS":
		return 7
	if region == "NA":
		return -16
	if region == "SA":
		return -16

def html_stripper(html):
	x = re.sub('<[^<]+?>', '', str(html)) #gotta coerce to string
	x = re.sub('\n', ' ', x)
	x = re.sub( '\s+', ' ', x).strip() #this removes all whitespace and makes single space
	return(x)

def convertRegion(region):
	if region == 'Southeast_Asia':
		return 'SEA'
	if region == 'China':
		return 'CN'
	if region == 'Western_Europe':
		return 'EU'
	if region == 'Eastern_Europe':
		return 'CIS'
	if region == 'North_America':
		return 'NA'
	if region == 'South_America':
		return 'SA'
	return ("Region not found for " + region)

def convertDiv(div):
	if (div == "Division_I"):
		return "Div1"
	else:
		return "Div2"

# adapted from https://github.com/c00kie17/liquipediapy and his parsing, thanks mate! Added a caching mechanism and
# function also returns a bool that states whether the cache was used, to know if we need to implement the 30s sleep
# in the next function, to abide by Liquipedia's terms of use wrt rate limiting.
def parse(page):
	url = 'https://liquipedia.net/dota2/api.php?action=parse&format=json&page='+page
	response = requests.get(url, headers=headers)
	isCached = response.from_cache

	if response.status_code == 200:
		try:
			page_html = response.json()['parse']['text']['*']
		except KeyError:
			raise Exception(response.json(),response.status_code)	
		soup = BeautifulSoup(page_html,features="lxml")
		redirect = soup.find('ul',class_="redirectText")
		if redirect is None:
			return soup,None,isCached
		else:
			redirect_value = soup.find('a').get_text()
			redirect_value = quote(redirect_value)
			soup,__ = parse(redirect_value)
			return soup,redirect_value,isCached
	else:
		raise Exception(response.json(),response.status_code)