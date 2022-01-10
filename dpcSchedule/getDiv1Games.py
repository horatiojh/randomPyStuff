from helpers import *

# setup cache
# requests_cache.install_cache(cache_name='scheduleCacheDiv1', backend='sqlite', expire_after=6000)

# Which week do we want to generate the schedule for 
week = 1

# filter teams we want to see
div1Teams = ['OG', 'Secret', 'Alliance', 'Tundra', 'Liquid', 'NGX', 'VP', 'TSpirit', 'EG', 'UND', 'QC', 'BOOM', 'TNC', 'MG.Trust', 'T1', 'IG', 'PSG.LGD', 'Aster', 'RNG', 'EHOME']

# pages with dpc schedule
regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']

# main code
urlListDiv1 = generate_div1_pages(regions)

schedule = createCompleteSchedule(urlListDiv1)
finalSchedule = getWeeklySchedule(schedule, week, div1Teams)
printScheduleToTerminal(finalSchedule)
