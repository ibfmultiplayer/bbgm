import json
import random

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
teams = export['teams']
d1_teams = list()
d2_teams = list()

for team in teams):
        if team['cid'] == 0:
                d1_teams.append(team['tid'])
        else:
                d2_teams.append(team['tid'])

# Randomise team order
d1_teams = random.sample(d1_teams, len(d1_teams))
d2_teams = random.sample(d2_teams, len(d2_teams))

def makeSchedule(d1_teams, d2_teams):
        # Makes a league schedule following the algorithm outlined at https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
        
        n = len(d1_teams) # assume d1 & d2 have equal size
        mid = int(n/2) # number of games per division per day
        schedule = list() # will store games here
        order = [0, n-1] # used to reorder the teams list each matchday

        for i in range(1, n-1):
                order.append(i)
        
        for i in range((n-1) * mid):
                index = i % mid
                if (((i+1) // mid) % 2) == 0: # alternates home/away teams to avoid long stretches at home/away
                        schedule.append({'homeTid':d1_teams[index], 'awayTid':d1_teams[-(index+1)]}) # add a match to the schedule
                        schedule.append({'homeTid':d2_teams[index], 'awayTid':d2_teams[-(index+1)]})
                else:
                        schedule.append({'homeTid':d1_teams[-(index+1)], 'awayTid':d1_teams[index]})
                        schedule.append({'homeTid':d2_teams[-(index+1)], 'awayTid':d2_teams[index]})
                if (i+1) % mid == 0: # reorder the teams lists at the end of a matchday
                        d1_teams = [d1_teams[j] for j in order]
                        d2_teams = [d2_teams[j] for j in order]
        
        return schedule

schedule = makeSchedule(d1_teams, d2_teams)

rev_schedule = list()
# Create the away legs
for match in schedule:
        rev_schedule.append({ 'homeTid':match['awayTid'], 'awayTid':match['homeTid'] })
        
# IBF has 4 rounds of fixtures
schedule = (schedule + rev_schedule) * 2

# Replace the existing schedule with our own
export['schedule'] = schedule

# Write to a bbgm league file
with open(filename, 'w') as outfile:
        json.dump(export, outfile)
