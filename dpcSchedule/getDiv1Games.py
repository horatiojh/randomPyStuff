from liquipediapy import liquipediapy, dota
import requests
import requests_cache
import re
from helpers import *

# setup cache
# requests_cache.install_cache(cache_name='scheduleCacheDiv1', backend='sqlite', expire_after=6000)

# Which week do we want to generate the schedule for 
week = 1

# filter teams we want to see
div1Teams = ['OG', 'Secret', 'Alliance', 'Tundra', 'Liquid', 'NGX', 'NAVI', 'VP', 'TSpirit', 'EG', 'UND', 'QC', 'BOOM', 'Fnatic', 'TNC', 'MG.Trust', 'OB.Neon', 'T1']

# pages with dpc schedule
regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']

# main code
# urlListDiv1 = generate_div1_pages(regions)

# schedule = createCompleteSchedule(urlListDiv1)
schedule = createCompleteSchedule(['Dota_Pro_Circuit/2021-22/1/Western_Europe/Division_I'])

getWeeklySchedule(schedule, week, div1Teams)
