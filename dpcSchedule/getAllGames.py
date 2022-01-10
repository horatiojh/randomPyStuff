from re import T
from helpers import *

# TODO: China schedule is on different timing, can figure how to do that -> can filter by date instead? 
# TODO: Refactor code so that if weekly schedule is wanted, it only fetches that week rather than everything 
# TODO: Add fixture if it's top of table teams (ranking-based)

# Which week do we want to generate the schedule for 
week = 5

# filter teams we want to see
div1Teams = ['OG', 'Secret', 'Alliance', 'Tundra', 'Liquid', 'NGX', 'VP', 'TSpirit', 'HR', 'EG', 'UND', 'QC', 'BOOM', 'Fnatic', 'MG.Trust', 'T1', 'SMG', 'IG', 'PSG.LGD', 'Aster', 'RNG', 'EHOME']
div2Teams = ['Xtreme', 'Bald', 'CF', 'CIS-R', 'NGX.SEA', 'Ragdoll', 'Polaris']

# pages with dpc schedule
regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']

# main code
urlListDiv1 = generate_div1_pages(regions)
urlListDiv2 = generate_div2_pages(regions)
urlList = urlListDiv1 + urlListDiv2
teams = div1Teams + div2Teams

schedule = createCompleteSchedule(urlList)
nonCNSchedule = getWeeklySchedule(schedule, week, teams)

# for the chinese ones (now that the schedule is not balanced; it's 3 weeks behind)
div1CNTeams = ['IG', 'PSG.LGD', 'Aster', 'RNG', 'EHOME']
cnWeek = week - 3
cnSchedule = getWeeklySchedule(schedule, cnWeek, div1CNTeams)
totalSchedule = nonCNSchedule + cnSchedule

printScheduleToTerminal(totalSchedule, week, True)



