import json
import random
import requests

''' 
------------------------------------------
'''
matchups = [[1,'bye'],[16,17],[9,'bye'],[8,'bye'],[5,'bye'],[12,'bye'],[13,20],[4,'bye'],[3,'bye'],[14,19],[11,'bye'],[6,'bye'],[7,'bye'],[10,'bye'],[15,18],[2,'bye']]
''' 
------------------------------------------
'''

cr = requests.get('https://raw.githubusercontent.com/ibfmultiplayer/bbgm/master/league_files/cupExport.json')
cr.encoding = 'utf-8-sig'
cup_export = json.loads(cr.text)

lr = requests.get('https://raw.githubusercontent.com/ibfmultiplayer/bbgm/master/league_files/ibfExport.json')
lr.encoding = 'utf-8-sig'
league_export = json.loads(lr.text)

rnd1_teams = list()
bye_teams = list()

for team in league_export['teams']:        
        if team['seasons'][-2]['playoffRoundsWon'] == -1:
                rnd1_teams.append(team['tid'])
        else:
                bye_teams.append(team['tid'])
                
rnd1_teams = random.sample(rnd1_teams, len(rnd1_teams))
bye_teams = random.sample(bye_teams, len(bye_teams))

draw = bye_teams + rnd1_teams

playoffs = list()
for match in matchups:
        series = dict()
        series['home'] = {'tid':draw[match[0]-1], 'cid':0, 'winp':0, 'seed':match[0], 'won':0}
        
        if match[1] != 'bye':
                series['away'] = {'tid':draw[match[1]-1], 'cid':0, 'winp':0, 'seed':match[1], 'won':0}
                
        playoffs.append(series)

year = int(league_export['meta']['phaseText'][:league_export['meta']['phaseText'].index(' ')])

cup_export['meta']['phaseText'] = league_export['meta']['phaseText'].replace('preseason', 'playoffs')
cup_export['meta']['name'] = 'IBF FA Cup ' + str(year)
cup_export['playoffSeries'].append({'season':year, 'currentRound':0, 'series':[playoffs,[],[],[],[]]})
cup_export['schedule'] = [{'homeTid':draw[15], 'awayTid':draw[16], 'day':1, 'gid':0},
                        {'homeTid':draw[12], 'awayTid':draw[19], 'day':1, 'gid':1},
                        {'homeTid':draw[13], 'awayTid':draw[18], 'day':1, 'gid':2},
                        {'homeTid':draw[14], 'awayTid':draw[17], 'day':1, 'gid':3}]
for lteam in league_export['teams']:
        for team in cup_export['teams']:
                if team['tid'] == lteam['tid']:
                        lteam['seasons'] == team['seasons']
                        lteam['stats'] == team['stats']
                        break
cup_export['teams'] = league_export['teams']
for x in cup_export['gameAttributes']:
        if x['key'] == 'phase':
                x['value'] = 3
        elif x['key'] == 'season':
                x['value'] = year
for lplayer in league_export['players']:
        for player in cup_export['players']:
                if player['pid'] == cup_player['pid']:
                        lplayer['awards'] = player['awards']
                        lplayer['injuries'] = player['injuries']
                        lplayer['stats'] = player['stats']
                        lplayer['statsTids'] = player['statsTids']
                        break
cup_export['players'] = league_export['players']
                
with open('cupExport.json', 'w') as outfile:
                outfile = json.dump(cup_export, outfile)
