import json
import random

'''
Generate a balanced league schedule for a single conference league
Write this schedule to the existing league file
'''

''' 
------------------------------------------
CHANGE FILENAME HERE
'''
filename = 'currentExport.json'
'''
------------------------------------------
'''

# Open json export file
with open(filename, 'r', encoding='utf-8-sig') as read_file:
        export = json.load(read_file)
        
# Get the team/division details
teams = list()
for team in export['teams']:
        teams.append(team['tid'])

# Randomise team order
teams = random.sample(teams, len(teams))

def makeSchedule(teams):
        # Makes a league schedule following the algorithm outlined at https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
        
        n = len(teams) # assume d1 & d2 have equal size
        mid = int(n/2) # number of games per division per day
        schedule = list() # will store games here
        order = [0, n-1] # used to reorder the teams list each matchday

        for i in range(1, n-1):
                order.append(i)
        
        for i in range((n-1) * mid):
                index = i % mid
                if (((i+1) // mid) % 2) == 0: # alternates home/away teams to avoid long stretches at home/away
                        schedule.append({'homeTid':teams[index], 'awayTid':teams[-(index+1)]}) # add a match to the schedule
                else:
                        schedule.append({'homeTid':teams[-(index+1)], 'awayTid':teams[index]})
                if (i+1) % mid == 0: # reorder the teams lists at the end of a matchday
                        teams = [teams[j] for j in order]
        
        return schedule

schedule = makeSchedule(teams)

rev_schedule = list()
# Create the away legs
for match in schedule:
        rev_schedule.append({ 'homeTid':match['awayTid'], 'awayTid':match['homeTid'] })
        
# IBF has 4 rounds of fixtures
schedule = (schedule + rev_schedule)

# Replace the existing schedule with our own
export['schedule'] = schedule

# Update game phase to regular season
export['meta']['phaseText'].replace('preseason', 'regular season')
for x in export['gameAttributes']:
        if x['key'] == 'phase':
                x['value'] = 1
                break

# Write to a bbgm league file
with open('ibfExport.json', 'w') as outfile:
        json.dump(export, outfile)
