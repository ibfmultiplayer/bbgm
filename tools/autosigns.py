import json
import csv
import re
import traceback
import operator
import random

'''
Generating free agent auto-signings and an updated league file

Instructions for use:
- Download the up to date league export and save in the same folder as this script
- Edit the filenames, market values and list of AI controlled teams as necessary below and run the script
- The updated league file 'ibfExport.json' will be generated
'''

def main():
        ''' 
        ------------------------------------------
        CHANGE FILENAME/MARKET VALUE HERE
        '''
        league_file = 'currentExport.json'
        
        # Set player market values, e.g. a player with overall rating between 80 & 100 is worth $50M
        market_value = { range(80, 101) : 50,
                         range(75, 80) : 35,
                         range(70, 75) : 25,
                         range(65, 70) : 17.5,
                         range(60, 65) : 10,
                         range(55, 60) : 5,
                         range(50, 55) : 2,
                         range(0, 50) : 1 }
                         
        AI_Teams = ['Fenerbache SK', 'Los Angeles Lakers', 'Punjab Steelers', 'Adelaide 36ers', 'Al Ahly', 'Bayi Rockets', 'Chicago Bulls', 'Limpopo Pride', 'Niigata Albirex', 'Panathinaikos B.C.', 'Primeiro de Agosto', 'Real Madrid']
        
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
                player['potential'] = player['ratings'][-1]['pot']
                
                if player['tid'] >= 0:
                        team_cash[player['tid']]['cash'] -= player['contract']['amount'] / 1000
                        team_cash[player['tid']]['roster'] += 1

        export['players'].sort(key = operator.itemgetter('potential'), reverse = True) 
        
        signings = list()
        
        for player in export['players']:
                
                if player['tid'] == -1:
                        for key in market_value.keys():
                                if player['overall'] in key:
                                        salary = market_value[key]
                        eligible_teams = list()
                        for tid in range(36):
                                if teams[tid] in AI_Teams:
                                        if team_cash[tid]['roster'] < 15:
                                                if salary == 1:
                                                        eligible_teams.append(tid)
                                                elif team_cash[tid]['cash'] >= salary:
                                                        eligible_teams.append(tid)
                                        
                                else:
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
                player.pop('potential')
                
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
