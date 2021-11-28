import re
from datetime import datetime, timedelta
from liquipediapy import liquipediapy, dota


# setup (token and stuff)
scriptName = "dpcSchedulerNew (horatiohotness@gmail.com)"
liquipy_object = liquipediapy(scriptName, 'dota2')

def generate_div1_pages(regionList):
	pages = []
	for region in regionList:
		tmp = 'Dota_Pro_Circuit/2021-22/1/' + region + '/Division_I'
		pages.append(tmp)
	return pages

def generate_div2_pages(regionList):
	pages = []
	for region in regionList:
		tmp = 'Dota_Pro_Circuit/2021-22/1/' + region + '/Division_II'
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
    tmp = soupObj.findAll("td", {"class":"matchlistslot"})
    teamRaw = html_stripper(tmp)
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

    # return list(zip(dateList, matchList))
    outputList = [': '.join(z) for z in zip(updatedDateList, matchList)]

    # return the week and the schedule
    return (week, outputList)


# generate a map of string lists, with each week as the key and the map as its value
def createCompleteScheduleForAUrl(inputUrl):

    print("Getting schedule from the following URL: " + inputUrl)
    region = re.search(r'/1/(.*)/Di', inputUrl).group(1)
    region = convertRegion(region)
    print('Region: ' + region)
    div = re.search(r'Division.*', inputUrl).group(0)
    div = convertDiv(div)
    print('Division: ' + div)

    output = {}
    soup,url = liquipy_object.parse(inputUrl)
    schedule = soup.findAll("table",{"class":"matchlist wikitable table table-bordered collapsible"})

    for week in schedule:
        weeklySchedule = getScheduleFromBSObject(week, region, div)
        output[weeklySchedule[0]] = weeklySchedule[1]

    return output

# now we do it for all regions, then we combine the maps to get one list for each week
def createCompleteSchedule(urlList):
    output = {}

    # collect individual schedules
    for url in urlList:
        tmp = createCompleteScheduleForAUrl(url)

        # add values to dict
        for week in tmp:
            if week in output:
                currVals = output[week] #list
                output[week] = currVals + tmp[week]
            else:
                output[week] = tmp[week]

    # sort the lists
    for week in output:
        output[week].sort()

    return output

# takes in 
def getWeeklySchedule(map, wkNumber, teams):
	week = "Week " + str(wkNumber)
	output = map[week]

	# if teams is empty means we want all matches
	if not teams:
		for item in output:
			print(item)
		return output
	
	# else match against the list provided
	else:
		filteredList = []
		for item in output:
			if any(team in item for team in teams):
				filteredList.append(item)
				print(item)
		return filteredList





def convertDateTime(dateString, region):
    timeToAdd = calculateRegionTimeDiff(region)
    format = '%B %d, %Y - %H:%M'
    tmp = datetime.strptime(dateString, format)
    newTime = tmp + timedelta(hours=timeToAdd)
    return newTime.strftime('%Y/%m/%d %H:%M')

def calculateRegionTimeDiff(region):
    if region == "SEA":
        return 0
    if region == "CN":
        return 0
    if region == "EU":
        return 7
    if region == "CIS":
        return 7
    if region == "NA":
        return 16
    if region == "SA":
        return 16

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
