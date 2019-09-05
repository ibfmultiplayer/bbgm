import json
import csv
import re
import traceback
import operator
import random

'''
Processing free agent signings from a summary csv and generating a league file
'''

def main():
        ''' 
        ------------------------------------------
        CHANGE FILENAME/MARKET VALUE HERE
        '''
        league_file = 'currentExport.json'
        
        market_value = { range(80, 101) : 50,
                         range(75, 80) : 40,
                         range(70, 75) : 30,
                         range(65, 70) : 20,
                         range(60, 65) : 15,
                         range(55, 60) : 7.5,
                         range(50, 55) : 4,
                         range(0, 50) : 1 }
        '''
        ------------------------------------------
        '''
        
        # Open json export file
        with open(league_file, 'r', encoding='utf-8-sig') as read_file:
                export = json.load(read_file)
                        
        year = int(export['meta']['phaseText'][:export['meta']['phaseText'].index(' ')])

        # Make a team name:tid dictionary to use in output file
        teams = { team['tid'] : team['region'] + ' ' + team['name'] for team in export['teams'] }
        
        team_cash = dict()
        
        for team in export['teams']:
                if team['cid'] == 0:
                        team_cash[team['tid']] = { 'cash' : 100, 'roster' : 0 }
                else:
                        team_cash[team['tid']] = { 'cash' : 75, 'roster' : 0 }
        
        for player in export['players']:
                player['overall'] = player['ratings'][-1]['ovr']
                player['sorting'] = player['overall'] - 2 * (year - player['born']['year'])
                
                if player['tid'] >= 0:
                        team_cash[player['tid']]['cash'] -= player['contract']['amount'] / 1000
                        team_cash[player['tid']]['roster'] += 1

        export['players'].sort(key = operator.itemgetter('sorting'), reverse = True) 
        
        signings = list()
        
        for player in export['players']:
                
                if player['tid'] == -1:
                        for key in market_value.keys():
                                if player['overall'] in key:
                                        salary = market_value[key]
                        eligible_teams = list()
                        for tid in range(36):
                                if team_cash[tid]['roster'] < 9:
                                        if salary == 1:
                                                eligible_teams.append(tid)
                                        elif team_cash[tid]['cash'] >= salary:
                                                eligible_teams.append(tid)
                                                
                        if len(eligible_teams) > 0:
                                player['tid'] = random.choice(eligible_teams)
                                player['contract']['amount'] = salary * 1000
                                player['contract']['exp'] = year + 1
                                team_cash[player['tid']]['cash'] -= salary
                                team_cash[player['tid']]['roster'] += 1
                                
                                signings.append(player['firstName'] + ' ' + player['lastName'] + ' signed with @' + teams[player['tid']] + ' on a 1 year ' + str(salary) + 'M contract')
                
                player.pop('overall')
                player.pop('sorting')
                
        for row in signings: 
                print(row)
        
        # write new league file
        with open('ibfExport.json', 'w') as outfile:
                outfile = json.dump(export, outfile)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
    finally:
        input('Press any key to close')
