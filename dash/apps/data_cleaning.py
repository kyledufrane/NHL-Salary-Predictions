# --------------------------------------------------------------
# Data Cleaning library
# --------------------------------------------------------------

# Import libaries needed for functions

import requests
import json
import pandas as pd
import pickle
import numpy as np
from bs4 import BeautifulSoup


##################################################################

def get_teams(team):
    '''This function takes in a dictionary, 'nhl_teams', from the NHL API created by 
    the requests library and returns a pandas dataframe of all the teams in the NHL (active & inactive)'''   

    # Initialize an empty dictionary
    teams = {}
    
    # Allow for iteration over the index values       
    for i in team.keys():
        
        # Initialize a sub dictionary so data is not overwritten
        teams[i] = {}
        
        # Create a for loop to 
        for keys in team[i].json()['teams'][0].keys():
            
            # Create a new dictionary object
            teams[i][keys] = team[i].json()['teams'][0][keys]
            
            # Filter by nested dictionary values
            nested_dict = ['venue', 'division', 'conference', 'franchise']
            
            # Iterate through nested dictionary values
            for nested in nested_dict:
                
                # Grab what values we want
                if keys == nested:
                    
                    # iterate through json files
                    for value in team[i].json()['teams'][0][keys].keys():
                        
                        # Add selected values to dictionary
                        teams[i][f'{nested}_{value}'] = team[i].json()['teams'][0][keys][value]
                        
                        # Select value we want
                        if value == 'timeZone':
                            
                            # Add value to dictionary
                            teams[i][f'venue_{value}'] = team[i].json()['teams'][0][keys][value]['id']
    
    
    # Convert dictionary to DataFrame
    teams_df = pd.DataFrame(teams, columns = teams.keys()).T
    
    # Drop unwanted values
    teams_df.drop(nested_dict, axis=1, inplace = True)
    
    return teams_df

##################################################################

def build_roster(roster):
    '''This function takes in a dictionary, 'nhl_team_roster', from the NHL API created
    by the requests library and returns a pandas dataframe of all players with associated
    team number based from the api'''
    
    # Initialize empy dictionary
    person_dict = {}
    
    # Allow for iteration over the index values (API team number)        
    for num in roster.keys():
        
        # Initialize a sub dictionary so data is not overwritten
        person_dict[num] = {}
        
        # Create a for loop that will loop over every teams roster due to varying amounts of total players     
        for player_index in range(0, len(roster[num].json()['roster'])):
            
            # Initialize a sub dictionary so data is not overwritten on a team level 
            person_dict[num][player_index] = {}
            
            # Create a for loop that will loop over all of the keys within the 'roster' nested dictionaries
            for key in roster[num].json()['roster'][player_index].keys():
                
                # Allow the function to iterate over the 'person' nested dictionary                         
                if key == 'person':
                    
                    # Looping over the 'person' nested dictionary
                    for person in roster[num].json()['roster'][player_index][key]:
                        
                        # Adding values to the dictionary
                        person_dict[num][player_index][person] = roster[num].json()['roster'][player_index][key][person]
                
                # Allow the function to iterate over the 'position' nested dictionary
                if key == 'position':
                    
                    # Looping over the 'position' nested dictionary
                    for position in roster[num].json()['roster'][player_index][key]:
                        
                        # Adding values to the dictionary
                        person_dict[num][player_index][position] = roster[num].json()['roster'][player_index][key][position]
                
                # Allow the function to add the jersey number to the dictionary
                if key == 'jerseyNumber':
                    
                    # Adding value to the dictionary
                    person_dict[num][player_index][key] = roster[num].json()['roster'][player_index][key]
        
    # Adding the API's team number as a value within the nested dictionaries in case we need to join on this value at a later time
    for value in person_dict:
        
        for length in range(0, len(person_dict[value])):
        
            person_dict[value][length]['Team_Number'] = value
        
    # Initializing an empty list to convert into a pandas dataframe
    df_list = []
    
    # Iterating over the above created dictionary
    for num in person_dict:
        
        # Create a for loop that will loop over every teams roster due to varying amounts of total players
        for length in range(0, len(person_dict[num])):
            
            # Appending values to dictionary
            df_list.append(person_dict[num][length])
    
    # Creating Pandas DataFrame
    roster_df = pd.DataFrame(df_list)  
        
    return roster_df

##################################################################

def player_statistics(df, player_stat):
    ''' This function takes in a dataframe and ditionary containing player stats
    by 'link' within the dataframe. The output concats the df with player stats pulled
    from the dictionary. The a few of the new columns include height, weight, nationality, current
    team, and position.
    
    '''
    # Initialize new dictionary                                                                                          
    player_dict = {}
    
    # Iterate through the link column (player specific)                                                            
    for link in df['link']:
        
        # Create new unique key in the dictionary                                                
        player_dict[link] = {}
        
        # Iterate through json file
        for info in player_stat[link].json()['people'][0].keys():
            
            # Add player info to dictionary
            player_dict[link][info] = player_stat[link].json()['people'][0][info]
            
            # Select wanted value
            if info == 'currentTeam':
                                
                # Iterate through json file
                for team in player_stat[link].json()['people'][0][info]:
                                                                                                
                    # Add value to dictionary
                    player_dict[link][f'current_team_{team}'] = player_stat[link].json()['people'][0][info][team]
            
            # Select wanted value            
            if info == 'primaryPosition':
                                                                                                              
                # Iterate through json file
                for position in player_stat[link].json()['people'][0][info]:
                                                                                                              
                    # Add value to dictionary
                    player_dict[link][f'primary_position_{position}'] = player_stat[link].json()['people'][0][info][position]
                 
    
                                                                                                              
    # Create player dataframe                                                                                
    player_df = pd.DataFrame(player_dict).T.reset_index()
                                                                                                              
    # Drop unwanted columns
    player_df.drop(['currentTeam', 'primaryPosition'], axis = 1, inplace = True)
                                                                                                              
    # Concat existing dataframe with newly created dataframe                  
    full_player_df = pd.concat([df, player_df], axis = 1, join='inner')

    
    return full_player_df

##################################################################

def player_stats_by_year(df, year):
    ''' This function takes in a dataframe and a season year (Ex. 20182019) 
    and returns a dictionary with player stats for that year'''

    # Create empty dictionary
    player_stats = {}

    # Iterate through dataframe by link (unique to each player)
    for link in df['link']:
            
            # Creat URL from API
            url = f'https://statsapi.web.nhl.com/{link}/stats?stats=statsSingleSeason&season={year}'

            headers = {
                'x-rapidapi-key': "c10092ada9mshd8d43cac6b3023cp1b369ajsn4c45f8f530d0",
                'x-rapidapi-host': "api-hockey.p.rapidapi.com"
            }
            
            # Add json to dictionary
            player_stats[link] = requests.request("GET", url, headers=headers)
            
    return player_stats

##################################################################

def extract_player_stats(df, player_dict):
    ''' This function takes in a dataframe and dictionary from the NHL players 
    API and returns a dataframe with all features from the JSON files'''
    
    # Create empty dictionary
    player = {}
     
    # Iterate through dataframe by link (unique to each player)   
    for link in player_dict.keys():
        
        # Attempt to pull information from JSON files
        try:
            
            # Create unique dictionary key
            player[link] = {}

            # Add season to dictionary
            player[link]['season'] = player_dict[link].json()['stats'][0]['splits'][0]['season']

            # Iterate through 'stat' key
            for stats in player_dict[link].json()['stats'][0]['splits'][0]['stat']:

                # Select all stats within the stats key
                player[link][stats] = player_dict[link].json()['stats'][0]['splits'][0]['stat'][stats]
    
        # Ignore all errors since we do not care about empty or null JSON objects
        except:

            pass
    
    player = {k: v for k, v in player.items() if v}
    
    # Convert to dataframe
    player_df = pd.DataFrame(player).T.reset_index()

    return player_df


                    
##################################################################