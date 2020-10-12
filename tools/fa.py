import json
import csv
import re
import traceback

'''
Processing free agent signings from a summary csv and generating a league file
'''

def main():
        ''' 
        ------------------------------------------
        CHANGE FILENAME HERE
        '''
        league_file = 'currentExport.json'
        fa_file = 'faSummary.csv'
        '''
        ------------------------------------------
        '''

        # Open json export file
        with open(league_file, 'r', encoding='utf-8-sig') as read_file:
                export = json.load(read_file)
                
                
        rows = list() # will store csv rows in a 2d list

        # Open csv signings file
        with open(fa_file, 'r', encoding='utf-8') as read_file:
                reader = csv.reader(read_file, delimiter = ',', quotechar = '"')
                
                for row in reader:
                        rows.append(row)

        keys = rows[0] # for converting signings to list of dictionaries
        signings = list()

        for row in rows[1:]:
                x = { key : row[keys.index(key)] for key in keys }
                if x['Sign'] =="Y": # anyone who didn't sign has empty string for this field
                        signings.append(x) # store the players who did sign
        
        if 'preseason' in export['meta']['phaseText']:
                year = int(export['meta']['phaseText'][:export['meta']['phaseText'].index(' ')]) - 1
        else:
                year = int(export['meta']['phaseText'][:export['meta']['phaseText'].index(' ')])
                        
        for signing in signings:
                
                signing['amount'] = int(float(signing['Salary'][signing['Salary'].index("$") + 2:signing['Salary'].index("M")]) * 1000)
                
                signing['exp'] = int(signing['Years']) + year
                
                # Any options/NTCs are stored in the player 'loc' field
                signing['locModifier'] = ''
                
                if signing['Option'] == 'PO':
                        signing['locModifier'] = ' - ' + str(signing['exp'] + 1) + ' PO'
                if signing['Option'] == 'TO':
                        signing['locModifier'] = ' - ' + str(signing['exp'] + 1) + ' TO'
                if signing['Option'] == '2PO':
                        signing['locModifier'] = ' - ' + str(signing['exp'] + 1) + ' PO/' + str(signing['exp'] + 2) + ' PO'
                if signing['Option'] == '2TO':
                        signing['locModifier'] = ' - ' + str(signing['exp'] + 1) + ' TO/' + str(signing['exp'] + 2) + ' TO'
                if signing['Option'] == 'PO/TO':
                        signing['locModifier'] = ' - ' + str(signing['exp'] + 1) + ' PO/' + str(signing['exp'] + 2) + ' TO'
                if signing['Option'] == 'TO/PO':
                        signing['locModifier'] = ' - ' + str(signing['exp'] + 1) + ' TO/' + str(signing['exp'] + 2) + ' PO'
                
                if (signing['Clause'] != 'None') and (signing['Clause'] != ''):
                        if signing['locModifier'] == '':
                                signing['locModifier'] = ' - (' + signing['Clause'] + ')'
                        else:
                                signing['locModifier'] += ' (' + signing['Clause'] + ')'

        # Make a team name:tid dictionary to use in output file
        teams = { team['region'] + ' ' + team['name'] : team['tid'] for team in export['teams'] }

        for player in export['players']: # update each player's contract info in the export
                
                for signing in signings:
                        
                        if player['firstName'] + ' ' + player['lastName'] == signing['Player']: # check if the player is in our list of signings
                                player['tid'] = teams[signing['Team']]
                                player['contract']['amount'] = signing['amount']
                                player['contract']['exp'] = signing['exp']
                                if '-' in player['college']: # loc has a '-' iff a player had options stored from a previous contract
                                        player['college'] = player['college'][:player['college'].index('-')] # remove previous options
                                player['college'] += signing['locModifier'] # add new options info
                                
                                if (signing['Clause'] == 'None') or (signing['Clause'] == ''):
                                        if signing['Years'] == '1':
                                                if signing['Option'] == 'None':
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' year, ' + signing['Salary'] + ' contract with @' + signing['Team'])
                                                else:
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' year + ' + signing['Option'] + ', ' + signing['Salary'] + ' contract with @' + signing['Team'])
                                        else:                             
                                                if signing['Option'] == 'None':
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' years, ' + signing['Salary'] + ' contract with @' + signing['Team'])
                                                else:
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' years + ' + signing['Option'] + ', ' + signing['Salary'] + ' contract with @' + signing['Team'])
                                else:
                                        if signing['Years'] == '1':
                                                if signing['Option'] == 'None':
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' year, ' + signing['Salary'] + ' contract (' + signing['Clause'] + ') with @' + signing['Team'])
                                                else:
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' year + ' + signing['Option'] + ', ' + signing['Salary'] + ' contract (' + signing['Clause'] + ') with @' + signing['Team'])
                                        else:                             
                                                if signing['Option'] == 'None':
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' years, ' + signing['Salary'] + ' contract (' + signing['Clause'] + ') with @' + signing['Team'])
                                                else:
                                                        print(signing['Player'] + ' signs a ' + signing['Years'] + ' years + ' + signing['Option'] + ', ' + signing['Salary'] + ' contract (' + signing['Clause'] + ') with @' + signing['Team'])
                                
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
