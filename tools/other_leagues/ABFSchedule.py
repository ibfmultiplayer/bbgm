import json
import random

'''
Generate a schedule as described by the suggestion on 08/15/19
'''

''' 
------------------------------------------
CHANGE FILENAME AND DIVISION MATCHUPS HERE
'''
filename = 'currentExport.json'
alignment = 1 #determines which divisions play each other (1, 2, or 3) - card
'''
------------------------------------------
'''

# Open json export file - alo
with open(filename, 'r', encoding='utf-8-sig') as read_file:
        export = json.load(read_file)
        
# Get the team/division details - alo
teams = export['teams']
d1_teams = list()
d2_teams = list()
d3_teams = list()
d4_teams = list()
d5_teams = list()
d6_teams = list()
d7_teams = list()
d8_teams = list()
all_teams = list()

for team in teams:
        if team['did'] == 0:
                d1_teams.append(team['tid'])
        elif team['did'] == 1:
                d2_teams.append(team['tid'])
        elif team['did'] == 2:
                d3_teams.append(team['tid'])
        elif team['did'] == 3:
                d4_teams.append(team['tid'])
        elif team['did'] == 4:
                d5_teams.append(team['tid'])
        elif team['did'] == 5:
                d6_teams.append(team['tid'])
        elif team['did'] == 6:
                d7_teams.append(team['tid'])
        else:
                d8_teams.append(team['tid'])

# Randomise team order - alo
d1_teams = random.sample(d1_teams, len(d1_teams))
d2_teams = random.sample(d2_teams, len(d2_teams))
d3_teams = random.sample(d3_teams, len(d3_teams))
d4_teams = random.sample(d4_teams, len(d4_teams))
d5_teams = random.sample(d5_teams, len(d5_teams))
d6_teams = random.sample(d6_teams, len(d6_teams))
d7_teams = random.sample(d7_teams, len(d7_teams))
d8_teams = random.sample(d8_teams, len(d8_teams))



def makeSchedule(d1_teams, d2_teams, d3_teams, d4_teams, d5_teams, d6_teams, d7_teams, d8_teams):
        # Makes a league schedule following the algorithm outlined at https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm - alo
        
        n = len(d1_teams) # each division has equal size - alo
        mid = int(n/2) # number of games per division per day - alo
        schedule = list() # will store games here - alo
        order = [0, n-1] # used to reorder the teams list each matchday - alo

        for i in range(1, n-1):
                order.append(i)
        
        for i in range((n-1) * mid):
                index = i % mid
                if (((i+1) // mid) % 2) == 0: # alternates home/away teams to avoid long stretches at home/away - alo
                        schedule.append({'homeTid':d1_teams[index], 'awayTid':d1_teams[-(index+1)]}) # add a match to the schedule - alo
                        schedule.append({'homeTid':d2_teams[index], 'awayTid':d2_teams[-(index+1)]})
                        schedule.append({'homeTid':d3_teams[index], 'awayTid':d3_teams[-(index+1)]})
                        schedule.append({'homeTid':d4_teams[index], 'awayTid':d4_teams[-(index+1)]})
                        schedule.append({'homeTid':d5_teams[index], 'awayTid':d5_teams[-(index+1)]})
                        schedule.append({'homeTid':d6_teams[index], 'awayTid':d6_teams[-(index+1)]})
                        schedule.append({'homeTid':d7_teams[index], 'awayTid':d7_teams[-(index+1)]})
                        schedule.append({'homeTid':d8_teams[index], 'awayTid':d8_teams[-(index+1)]})
                else:
                        schedule.append({'homeTid':d1_teams[-(index+1)], 'awayTid':d1_teams[index]})
                        schedule.append({'homeTid':d2_teams[-(index+1)], 'awayTid':d2_teams[index]})
                        schedule.append({'homeTid':d3_teams[-(index+1)], 'awayTid':d3_teams[index]})
                        schedule.append({'homeTid':d4_teams[-(index+1)], 'awayTid':d4_teams[index]})
                        schedule.append({'homeTid':d5_teams[-(index+1)], 'awayTid':d5_teams[index]})
                        schedule.append({'homeTid':d6_teams[-(index+1)], 'awayTid':d6_teams[index]})
                        schedule.append({'homeTid':d7_teams[-(index+1)], 'awayTid':d7_teams[index]})
                        schedule.append({'homeTid':d8_teams[-(index+1)], 'awayTid':d8_teams[index]})
                if (i+1) % mid == 0: # reorder the teams lists at the end of a matchday - alo
                        d1_teams = [d1_teams[j] for j in order]
                        d2_teams = [d2_teams[j] for j in order]
                        d3_teams = [d3_teams[j] for j in order]
                        d4_teams = [d4_teams[j] for j in order]
                        d5_teams = [d5_teams[j] for j in order]
                        d6_teams = [d6_teams[j] for j in order]
                        d7_teams = [d7_teams[j] for j in order]
                        d8_teams = [d8_teams[j] for j in order]

        for i in range((n-1) * mid): #just sort of copied this to make it work the way i wanted it to /shrug - card
                index = i % mid
                if (((i+1) // mid) % 2) == 0: # alternates home/away teams to avoid long stretches at home/away -  alo
                        schedule.append({'homeTid':d1_teams[index], 'awayTid':d1_teams[-(index+1)]}) # add a match to the schedule - alo
                        schedule.append({'homeTid':d2_teams[index], 'awayTid':d2_teams[-(index+1)]})
                        schedule.append({'homeTid':d3_teams[index], 'awayTid':d3_teams[-(index+1)]})
                        schedule.append({'homeTid':d4_teams[index], 'awayTid':d4_teams[-(index+1)]})
                        schedule.append({'homeTid':d5_teams[index], 'awayTid':d5_teams[-(index+1)]})
                        schedule.append({'homeTid':d6_teams[index], 'awayTid':d6_teams[-(index+1)]})
                        schedule.append({'homeTid':d7_teams[index], 'awayTid':d7_teams[-(index+1)]})
                        schedule.append({'homeTid':d8_teams[index], 'awayTid':d8_teams[-(index+1)]})
                else:
                        schedule.append({'homeTid':d1_teams[-(index+1)], 'awayTid':d1_teams[index]})
                        schedule.append({'homeTid':d2_teams[-(index+1)], 'awayTid':d2_teams[index]})
                        schedule.append({'homeTid':d3_teams[-(index+1)], 'awayTid':d3_teams[index]})
                        schedule.append({'homeTid':d4_teams[-(index+1)], 'awayTid':d4_teams[index]})
                        schedule.append({'homeTid':d5_teams[-(index+1)], 'awayTid':d5_teams[index]})
                        schedule.append({'homeTid':d6_teams[-(index+1)], 'awayTid':d6_teams[index]})
                        schedule.append({'homeTid':d7_teams[-(index+1)], 'awayTid':d7_teams[index]})
                        schedule.append({'homeTid':d8_teams[-(index+1)], 'awayTid':d8_teams[index]})
                if (i+1) % mid == 0: # reorder the teams lists at the end of a matchday - alo
                        d1_teams = [d1_teams[j] for j in order]
                        d2_teams = [d2_teams[j] for j in order]
                        d3_teams = [d3_teams[j] for j in order]
                        d4_teams = [d4_teams[j] for j in order]
                        d5_teams = [d5_teams[j] for j in order]
                        d6_teams = [d6_teams[j] for j in order]
                        d7_teams = [d7_teams[j] for j in order]
                        d8_teams = [d8_teams[j] for j in order]

        if alignment == 1: # division matchups - card
                for i in range(0,n):
                        for j in range(0,n):
                                schedule.append({'homeTid':d1_teams[i], 'awayTid':d2_teams[j]})
                                schedule.append({'homeTid':d3_teams[i], 'awayTid':d4_teams[j]})
                                schedule.append({'homeTid':d5_teams[i], 'awayTid':d6_teams[j]})
                                schedule.append({'homeTid':d7_teams[i], 'awayTid':d8_teams[j]})    
        elif alignment == 2:
                for i in range(0,n):
                        for j in range(0,n):
                                schedule.append({'homeTid':d1_teams[i], 'awayTid':d3_teams[j]})
                                schedule.append({'homeTid':d2_teams[i], 'awayTid':d4_teams[j]})
                                schedule.append({'homeTid':d5_teams[i], 'awayTid':d7_teams[j]})
                                schedule.append({'homeTid':d6_teams[i], 'awayTid':d8_teams[j]})
        elif alignment == 3:
                for i in range(0,n):
                        for j in range(0,n):
                                schedule.append({'homeTid':d1_teams[i], 'awayTid':d4_teams[j]})
                                schedule.append({'homeTid':d3_teams[i], 'awayTid':d2_teams[j]})
                                schedule.append({'homeTid':d5_teams[i], 'awayTid':d8_teams[j]})
                                schedule.append({'homeTid':d7_teams[i], 'awayTid':d6_teams[j]})

        all_teams = d1_teams + d2_teams + d3_teams + d4_teams + d5_teams + d6_teams + d7_teams + d8_teams #used to make all-league round robin - liam

        n = len(all_teams) #gotta change all this stuff to match the new array size - card
        mid = int(n/2) 
        order = [0, n-1]

        for i in range(1, n-1):
                order.append(i)

        for i in range(31 * 16):
                index = i % mid
                if (((i+1) // mid) % 2) == 0: # alternates home/away teams to avoid long stretches at home/away - alo
                        schedule.append({'homeTid':all_teams[index], 'awayTid':all_teams[31-index]}) # add a match to the schedule - alo
                else:
                        schedule.append({'homeTid':all_teams[31-index], 'awayTid':all_teams[index]})
                if (i+1) % mid == 0: # reorder the teams lists at the end of a matchday - alo
                        all_teams = [all_teams[j] for j in order]

        return schedule

schedule = makeSchedule(d1_teams, d2_teams, d3_teams, d4_teams, d5_teams, d6_teams, d7_teams, d8_teams)



rev_schedule = list()
# Create the away legs - alo
for match in schedule:
        rev_schedule.append({ 'homeTid':match['awayTid'], 'awayTid':match['homeTid'] })

schedule = schedule + rev_schedule

schedule.append({'homeTid':-1, 'awayTid':-2})
        
# Replace the existing schedule with our own - alo
export['schedule'] = schedule

# Update game phase to regular season - alo
export['meta']['phaseText'].replace('preseason', 'regular season')
for x in export['gameAttributes']:
        if x['key'] == 'phase':
                x['value'] = 1
                break

# Write to a bbgm league file - alo
with open('abfExport.json', 'w') as outfile:
        json.dump(export, outfile)
