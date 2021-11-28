from liquipediapy import liquipediapy, dota
import requests
import re
from helpers import *

# Which week do we want to generate the schedule for 
week = 1

# filter teams we want to see
div1Teams = ['OG', 'Secret', 'Alliance', 'Tundra', 'Liquid', 'NAVI', 'VP', 'TSpirit', 'EG', 'UND', 'QC', 'BOOM', 'Fnatic', 'TNC', 'MG.Trust', 'OB.Neon', 'T1']
div2Teams = ['Talon', 'Bald', 'CIS Rejects', 'Xtreme']

# pages with dpc schedule
regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']

# main code
urlListDiv1 = generate_div1_pages(regions)
urlListDiv2 = generate_div2_pages(regions)
urlList = urlListDiv1 + urlListDiv2
teams = div1Teams + div2Teams

schedule = createCompleteSchedule(urlList)
getWeeklySchedule(schedule, week, teams)



# TODO: China schedule is on different timing, can figure how to do that 

# TODO: Refactor code so that if weekly schedule is wanted, it only fetches that week rather than everything 

# TODO: Parse date back nicely 

# TODO: Add fixture if it's top of table teams (ranking-based)