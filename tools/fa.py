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
                if x['Wave Raw Output'] != "": # anyone who didn't sign has empty string for this field
                        signings.append(x) # store the players who did sign
        
        if 'Preseason' in export['meta']['phaseText']:
                year = int(export['meta']['phaseText'][:export['meta']['phaseText'].index(' ')]) + 1
        else:
                year = int(export['meta']['phaseText'][:export['meta']['phaseText'].index(' ')])
                        
        for signing in signings: # convert summary column Yrs/$M into salary amount, contract years & any options
                
                # Anything between '/' and 'M' is our annual salary
                signing['amount'] = int(float(signing['Yrs/$M'][signing['Yrs/$M'].index("/") + 1:signing['Yrs/$M'].index("M")]) * 1000)
                
                # + means there is a player/team option
                if '+' in signing['Yrs/$M']:
                        signing['exp'] = int(signing['Yrs/$M'][:signing['Yrs/$M'].index("+")]) + year
                else:
                        signing['exp'] = int(signing['Yrs/$M'][:signing['Yrs/$M'].index("/")]) + year
                
                # Any options/NTCs are stored in the player 'loc' field
                signing['locModifier'] = ''
                multi_option = re.search('\d((PO)|(TO))', signing['Yrs/$M']) # A number before PO/TO means it is for multiple years
                if multi_option:
                        option_start = signing['exp'] + 1 # options start the year after expiry
                        option_end = int(multi_option.group(0)[0]) + signing['exp'] # get number of option years and add it to expiry year
                        option_type = multi_option.group(0)[1:] # get option type (PO/TO) from matched pattern
                        # add option info to our modifier
                        signing['locModifier'] += ' - ' + str(option_start)[2:] + '-' + str(option_end)[2:] + ' ' + option_type
                        
                elif 'PO' in signing['Yrs/$M']: # as above but for single year options
                        option_start = signing['exp'] + 1
                        option_type = 'PO'
                        
                        signing['locModifier'] += ' - ' + str(option_start)[2:] + ' ' + option_type
                        
                elif 'TO' in signing['Yrs/$M']: # as above but for single year options
                        option_start = signing['exp'] + 1
                        option_type = 'TO'
                        
                        signing['locModifier'] += ' - ' + str(option_start)[2:] + ' ' + option_type
                
                if 'NTC' in signing['Yrs/$M']:
                        signing['locModifier'] += ' NTC'
                if 'NLC' in signing['Yrs/$M']:
                        signing['locModifier'] += ' NLC'

        # Make a team name:tid dictionary to use in output file
        teams = { team['region'] + ' ' + team['name'] : team['tid'] for team in export['teams'] }

        for player in export['players']: # update each player's contract info in the export
                
                for signing in signings:
                        
                        if player['firstName'] + ' ' + player['lastName'] == signing['Player name']: # check if the player is in our list of signings
                                player['tid'] = teams[signing['Team']]
                                player['contract']['amount'] = signing['amount']
                                player['contract']['exp'] = signing['exp']
                                if '-' in player['born']['loc']: # loc has a '-' iff a player had options stored from a previous contract
                                        player['born']['loc'] = player['born']['loc'][:player['born']['loc'].index('-')] # remove previous options
                                player['born']['loc'] += signing['locModifier'] # add new options info
                                
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
