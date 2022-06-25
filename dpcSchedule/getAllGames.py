from re import T
from helpers import *

# TODO: China schedule is on different timing, can figure how to do that -> can filter by date instead? 
# TODO: Refactor code so that if weekly schedule is wanted, it only fetches that week rather than everything 
# TODO: Add fixture if it's top of table teams (ranking-based)

# Which week do we want to generate the schedule for 
season = 3
week = 4


# filter teams we want to see
div1Teams = ['OG', 'Secret', 'Tundra', 'Liquid', 'EG', 'UND', 'QC', 'BOOM', 'Fnatic', 'T1', 'PSG.LGD', 'Aster', 'RNG', 'Xtreme', 'NAVI', 'TSpirit'] 
div2Teams = ['NGX', 'Bald']

# pages with dpc schedule
div1Regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']
div2Regions = ['Western_Europe','China','Southeast_Asia']

# main code
urlListDiv1 = generate_pages(1, div1Regions, season)
urlListDiv2 = generate_pages(2, div2Regions, season)
urlList = urlListDiv1 + urlListDiv2
teams = div1Teams + div2Teams

schedule = createCompleteSchedule(urlList, season)
# print(schedule)
weeklySchedule = getWeeklySchedule(schedule, week, teams)
# print(weeklySchedule)
printScheduleToTerminal(weeklySchedule, week, True)



