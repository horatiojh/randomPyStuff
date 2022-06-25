from helpers import *

# Which week do we want to generate the schedule for 
week = 1

# filter teams we want to see
div2Teams = ['Talon', 'Xtreme', 'Bald', 'CIS-R', 'NGX.SEA']

# pages with dpc schedule
regions = ['Western_Europe','Eastern_Europe','China','Southeast_Asia','North_America','South_America']

# main code
urlListDiv2 = generate_div2_pages(regions)
schedule = createCompleteSchedule(urlListDiv2)
finalSchedule = getWeeklySchedule(schedule, week, div2Teams)
printScheduleToTerminal(finalSchedule)
