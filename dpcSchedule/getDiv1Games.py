from liquipediapy import liquipediapy, dota
import requests
import re
from helpers import *

# Which week do we want to generate the schedule for 
week = 1

# filter teams we want to see
div1Teams = ['OG', 'Secret', 'Alliance', 'Tundra', 'Liquid', 'NAVI', 'VP', 'TSpirit', 'EG', 'UND', 'QC', 'BOOM', 'Fnatic', 'TNC', 'MG.Trust', 'OB.Neon', 'T1']

# pages with dpc schedule
regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']

# main code
urlListDiv1 = generate_div1_pages(regions)

schedule = createCompleteSchedule(urlListDiv1)
getWeeklySchedule(schedule, week, div1Teams)