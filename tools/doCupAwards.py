import json
import operator

''' 
------------------------------------------
'''
league_file = "cupExport.json"
''' 
------------------------------------------
'''

with open(league_file, 'r', encoding = 'utf-8-sig') as read_file:
        export = json.load(read_file)
        
year = int(export['meta']['phaseText'][:export['meta']['phaseText'].index(' ')])
        
# Find and replace best team record
team_records = []
for team in export['teams']:        
        x = {'tid':team['tid'],
             'abbrev':team['abbrev'],
             'region':team['region'],
             'name':team['name'],
             'won':0,
             'lost':0}
             
        team_records.append(x)
             
team_records.sort(key = operator.itemgetter('tid'), reverse = False)
             
for game in export['games']:
        team_records[game['won']['tid']]['won'] += 1
        team_records[game['lost']['tid']]['lost'] += 1
        
for i in range(len(export['teams'])):
        team_records[i]['winp'] = team_records[i]['won'] / (team_records[i]['won'] + team_records[i]['lost'])
        
team_records.sort(key = operator.itemgetter('winp'), reverse = True)

export['awards'][-1]['bestRecord'] = {'tid':team_records[0]['tid'],
                                      'abbrev':team_records[0]['abbrev'],
                                      'region':team_records[0]['region'],
                                      'name':team_records[0]['name'],
                                      'won':team_records[0]['won'],
                                      'lost':team_records[0]['lost']}
                                      
export['awards'][-1]['bestRecordConfs'] = [{'tid':team_records[0]['tid'],
                                            'abbrev':team_records[0]['abbrev'],
                                            'region':team_records[0]['region'],
                                            'name':team_records[0]['name'],
                                            'won':team_records[0]['won'],
                                            'lost':team_records[0]['lost']}]
                                            
for team in team_records:
        export['teams'][team['tid']]['seasons'][-1]['won'] = team['won']
        export['teams'][team['tid']]['seasons'][-1]['wonDiv'] = team['won']
        export['teams'][team['tid']]['seasons'][-1]['wonConf'] = team['won']
        export['teams'][team['tid']]['seasons'][-1]['lost'] = team['lost']
        export['teams'][team['tid']]['seasons'][-1]['lostDiv'] = team['lost']
        export['teams'][team['tid']]['seasons'][-1]['lostConf'] = team['lost']

# Calculate player scores for each award
player_records = []
for player in export['players']:
        if player['stats'] !=  []:
                if (player['stats'][-1]['gp'] > 0) & (player['stats'][-1]['season'] == year):
                        x = {'pid':player['pid'],
                             'name':player['firstName'] + " " + player['lastName'],
                             'tid':player['stats'][-1]['tid'],
                             'abbrev':export['teams'][player['stats'][-1]['tid']]['abbrev'],
                             'pts':player['stats'][-1]['pts']/player['stats'][-1]['gp'],
                             'trb':(player['stats'][-1]['drb']+player['stats'][-1]['orb'])/player['stats'][-1]['gp'],
                             'ast':player['stats'][-1]['ast']/player['stats'][-1]['gp'],
                             'blk':player['stats'][-1]['blk']/player['stats'][-1]['gp'],
                             'stl':player['stats'][-1]['stl']/player['stats'][-1]['gp'],
                             'mvp':player['stats'][-1]['ewa'] + player['stats'][-1]['ows'] + player['stats'][-1]['dws'],
                             'roy':player['stats'][-1]['ewa'] + player['stats'][-1]['ows'] + player['stats'][-1]['dws'] + (player['stats'][-1]['pts']/(player['stats'][-1]['gp']*10)),
                             'dpoy':player['stats'][-1]['dws'] + ((player['stats'][-1]['stl'] + player['stats'][-1]['blk'])/(player['stats'][-1]['gp']*10)),
                             'smoy_elig':player['stats'][-1]['gs'] * 2 < player['stats'][-1]['gp'],
                             'roy_elig':player['draft']['year'] == int(year) - 1}
                             
                        player_records.append(x)
        
        player['awards'] = [x for x in player['awards'] if (x['season'] != year) | (x['type'] in ['Finals MVP', 'Won Championship'])]
        
# Award MVP
player_records.sort(key = operator.itemgetter('mvp'), reverse = True)
export['awards'][-1]['mvp'] = {'pid':player_records[0]['pid'],
                               'name':player_records[0]['name'],
                               'tid':player_records[0]['tid'],
                               'abbrev':player_records[0]['abbrev'],
                               'pts':player_records[0]['pts'],
                               'trb':player_records[0]['trb'],
                               'ast':player_records[0]['ast']}

# Award All-League Teams
export['awards'][-1]['allLeague'] = [{'title':'First Team', 'players':[]},
                                     {'title': 'Second Team', 'players':[]},
                                     {'title': 'Third Team', 'players':[]}]
i = 0
for player in player_records[:15]:
        x = {'pid':player['pid'],
             'name':player['name'],
             'tid':player['tid'],
             'abbrev':player['abbrev'],
             'pts':player['pts'],
             'trb':player['trb'],
             'ast':player['ast']}
             
        if i == 0:
                export['awards'][-1]['allLeague'][0]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'Most Valuable Player'})
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'First Team All-League'})
        elif i < 5:
                export['awards'][-1]['allLeague'][0]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'First Team All-League'})
        elif i < 10:
                export['awards'][-1]['allLeague'][1]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'Second Team All-League'})
        else:
                export['awards'][-1]['allLeague'][2]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'Third Team All-League'})
        i += 1

# Filter by eligibility and award Sixth Man of the Year
smoy_records = [x for x in player_records if x['smoy_elig']]
export['awards'][-1]['smoy'] = {'pid':smoy_records[0]['pid'],
                               'name':smoy_records[0]['name'],
                               'tid':smoy_records[0]['tid'],
                               'abbrev':smoy_records[0]['abbrev'],
                               'pts':smoy_records[0]['pts'],
                               'trb':smoy_records[0]['trb'],
                               'ast':smoy_records[0]['ast']}
                               
export['players'][smoy_records[0]['pid']]['awards'].append({'season':year, 'type':'Sixth Man of the Year'})
                               
# Award Defensive player
player_records.sort(key = operator.itemgetter('dpoy'), reverse = True)
export['awards'][-1]['dpoy'] = {'pid':player_records[0]['pid'],
                               'name':player_records[0]['name'],
                               'tid':player_records[0]['tid'],
                               'abbrev':player_records[0]['abbrev'],
                               'trb':player_records[0]['trb'],
                               'blk':player_records[0]['blk'],
                               'stl':player_records[0]['stl']}
                               
# Award All-Defensive Teams
export['awards'][-1]['allDefensive'] = [{'title':'First Team', 'players':[]},
                                     {'title': 'Second Team', 'players':[]},
                                     {'title': 'Third Team', 'players':[]}]
i = 0
for player in player_records[:15]:
        x = {'pid':player['pid'],
             'name':player['name'],
             'tid':player['tid'],
             'abbrev':player['abbrev'],
             'trb':player['trb'],
             'blk':player['blk'],
             'stl':player['stl']}
        
        if i == 0:
                export['awards'][-1]['allDefensive'][0]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'Defensive Player of the Year'})
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'First Team All-Defensive'})
        elif i < 5:
                export['awards'][-1]['allDefensive'][0]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'First Team All-Defensive'})
        elif i < 10:
                export['awards'][-1]['allDefensive'][1]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'Second Team All-Defensive'})
        else:
                export['awards'][-1]['allDefensive'][2]['players'].append(x)
                export['players'][player['pid']]['awards'].append({'season':year, 'type':'Third Team All-Defensive'})
        i += 1

# Filter by eligibility and award rookie of the year
roy_records = [x for x in player_records if x['roy_elig']]
roy_records.sort(key = operator.itemgetter('roy'), reverse = True)
export['awards'][-1]['roy'] = {'pid':roy_records[0]['pid'],
                               'name':roy_records[0]['name'],
                               'tid':roy_records[0]['tid'],
                               'abbrev':roy_records[0]['abbrev'],
                               'pts':roy_records[0]['pts'],
                               'trb':roy_records[0]['trb'],
                               'ast':roy_records[0]['ast']}
export['players'][roy_records[0]['pid']]['awards'].append({'season':year, 'type':'Rookie of the Year'})

# Award All-Rookie Team
export['awards'][-1]['allRookie'] = []
for player in roy_records[:5]:
        x = {'pid':player['pid'],
             'name':player['name'],
             'tid':player['tid'],
             'abbrev':player['abbrev'],
             'trb':player['trb'],
             'blk':player['blk'],
             'stl':player['stl']}
        
        export['awards'][-1]['allRookie'].append(x)
        export['players'][player['pid']]['awards'].append({'season':year, 'type':'All-Rookie Team'})
        
export['awards'][-1].pop('mip', None)

with open('cupExport.json', 'w') as out_file:
        out_file = json.dump(export, out_file)
