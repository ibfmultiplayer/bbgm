import json
import random

league_file = 'currentExport.json'
fixture_rounds = 4

with open(league_file, 'r', encoding='utf-8-sig') as read_file:
        export = json.load(read_file)
        
teams = export['teams']

cids = set()
for team in teams:
        cids.add(team['cid'])

all_teams = list()

for cid in cids:
        conf_teams = list()
        for team in teams:
                if team['cid'] == cid:
                        conf_teams.append(team['tid'])
        all_teams.append(random.sample(conf_teams, len(conf_teams)))


def make_schedule(teams):
        schedule = list()
        
        if len(teams) % 2 == 1:
                teams.append("None")
        
        num_rounds = len(teams) - 1
        
        for i in range(num_rounds):
                mid = int(len(teams) / 2)
                teams1 = teams[:mid]
                teams2 = teams[mid:]
                teams2.reverse()
                
                for j in range(len(teams1)):
                        if teams1[j] != "None" and teams2[j] != "None":
                                if (i % 2 == 0):
                                        schedule.append({'homeTid':teams1[j], 'awayTid':teams2[j], 'day':i+1})
                                else:
                                        schedule.append({'homeTid':teams2[j], 'awayTid':teams1[j], 'day':i+1})
                
                teams.insert(1, teams.pop())
        
        return schedule

all_schedules = list()
days = 0
for conf in all_teams:
        conf_schedule = make_schedule(conf)
        all_schedules.append(conf_schedule)
        if conf_schedule[-1]['day'] > days:
                days = conf_schedule[-1]['day']
                
combined_schedule = list()                

for i in range(days):
        for conf_schedule in all_schedules:
                for game in conf_schedule:
                        if game['day'] == i + 1:
                                combined_schedule.append(game)

for game in combined_schedule:
        del game['day']

reverse_schedule = list()
for game in combined_schedule:
        reverse_schedule.append({'homeTid':game['awayTid'], 'awayTid':game['homeTid']})
        
if fixture_rounds % 2 == 1:
        final_schedule = (combined_schedule + reverse_schedule) * int((fixture_rounds - 1) / 2) + combined_schedule
else:
        final_schedule = (combined_schedule + reverse_schedule) * int(fixture_rounds / 2)

export['schedule'] = final_schedule

export['meta']['phaseText'].replace('preseason', 'regular season')
for x in export['gameAttributes']:
        if x['key'] == 'phase':
                x['value'] = 1
                break

with open('schedule_export.json', 'w') as outfile:
        json.dump(export, outfile)
