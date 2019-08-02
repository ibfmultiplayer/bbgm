import json
import csv
import re

'''
Generate a csv file containing any players with player/team options and their contract details for the current season
'''

''' 
------------------------------------------
CHANGE FILENAME AND CURRENT YEAR HERE
'''
filename = 'currentExport.json'
year = 2109
'''
------------------------------------------
'''

# Open json export file
with open(filename, 'r', encoding='utf-8-sig') as read_file:
        export = json.load(read_file)

# We only need the player details
players = export['players']

# We will store contract info here
contracts = list()

# Add the headings as the first row of the contract list
headings = ['Name', 'Team', 'Salary', 'Option', 'Option Years']
contracts.append(headings)

# Make a team code:team name dictionary to use in output file
teams = { team['tid'] : team['region'] + ' ' + team['name'] for team in export['teams'] }

# Iterate through each player and store their info
for player in players:
        info = list()
        
        if (player['tid'] >= 0) & (int(player['contract']['exp']) == year) & ('PO' in player['born']['loc'] or 'TO' in player['born']['loc']): # We only want active players who expire this season
                
                info.append(player['firstName'] + " " + player['lastName']) # Player Name
                
                info.append(teams[player['tid']]) # Player team
                
                info.append("$" + str(player['contract']['amount'] / 1000) + "M") # Player Contract
                
                # Get contract option status from location field
                if 'PO' in player['born']['loc']:
                        info.append('Player')
                elif 'TO' in player['born']['loc']:
                        info.append('Team')
                else:
                        info.append('None')
                
                match = re.search('\d\d-\d\d', player['born']['loc'])
                if match:
                        info.append(match.group(0))
                else:
                        info.append(year + 1)
                
                contracts.append(info) # Add info for this player to our list

# Write contract info to csv
with open('options.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(contracts)
