
# from matplotlib import pyplot as plt

import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def clean_data():
    df = pd.read_csv('https://raw.githubusercontent.com/kyledufrane/NHL-Salary-Predictions/main/data/ml_cleaned_forward_players_df.csv')

    drop = [
        'birthCity',
        'birthDate',
        'Unnamed: 0',
        'index',
        'birthStateProvince',
        'height'
    ]

    df.drop(drop, axis=1, inplace=True)

    years = ['17', '18', '19', '20', '21', '22']
    columns_ = [col for col in df.select_dtypes(['int', 'float']).columns 
                if 'Salary' not in col and 'Pct' not in col
                if '22' in col
                or '21' in col
                or '20' in col
                or '19' in col
                or '18' in col
                or '17' in col]

    cleaned_names = [col_name[:-2] for col_name in columns_]
    unique_names = list(set(cleaned_names))
    shortHandedPoints = []
    powerPlayGoals = []
    powerPlayTimeOnIcePerGame = []
    shortHandedTimeOnIce = []
    shortHandedGoals = []
    evenTimeOnIce = []
    shortHandedTimeOnIcePerGame = []
    penaltyMinutes = []
    gameWinningGoals = []
    timeOnIcePerGame = []
    assists = []
    blocked = []
    points = []
    hits = []
    shifts = []
    powerPlayTimeOnIce = []
    plusMinus = []
    powerPlayPoints = []
    evenTimeOnIcePerGame = []
    goals = []
    overTimeGoals = []
    pim = []
    games = []
    timeOnIce = []
    shots = []

    for year in years:
        for col_name in unique_names:
            if col_name == 'shortHandedPoints':
                shortHandedPoints.append(f'{col_name}{year}')
            elif col_name == 'powerPlayGoals':
                powerPlayGoals.append(f'{col_name}{year}')
            elif col_name == 'powerPlayTimeOnIcePerGame':
                powerPlayTimeOnIcePerGame.append(f'{col_name}{year}')
            elif col_name == 'shortHandedTimeOnIce':
                shortHandedTimeOnIce.append(f'{col_name}{year}')
            elif col_name == 'shortHandedGoals':
                shortHandedGoals.append(f'{col_name}{year}')
            elif col_name == 'evenTimeOnIce':
                evenTimeOnIce.append(f'{col_name}{year}')
            elif col_name == 'shortHandedTimeOnIcePerGame':
                shortHandedTimeOnIcePerGame.append(f'{col_name}{year}')
            elif col_name == 'penaltyMinutes':
                penaltyMinutes.append(f'{col_name}{year}')
            elif col_name == 'gameWinningGoals':
                gameWinningGoals.append(f'{col_name}{year}')
            elif col_name == 'timeOnIcePerGame':
                timeOnIcePerGame.append(f'{col_name}{year}')
            elif col_name == 'assists':
                assists.append(f'{col_name}{year}')
            elif col_name == 'blocked':
                blocked.append(f'{col_name}{year}')
            elif col_name == 'points':
                points.append(f'{col_name}{year}')
            elif col_name == 'hits':
                hits.append(f'{col_name}{year}')
            elif col_name == 'shifts':
                shifts.append(f'{col_name}{year}')
            elif col_name == 'powerPlayTimeOnIce':
                powerPlayTimeOnIce.append(f'{col_name}{year}')
            elif col_name == 'plusMinus':
                plusMinus.append(f'{col_name}{year}')
            elif col_name == 'powerPlayPoints':
                powerPlayPoints.append(f'{col_name}{year}')
            elif col_name == 'evenTimeOnIcePerGame':
                evenTimeOnIcePerGame.append(f'{col_name}{year}')
            elif col_name == 'goals':
                goals.append(f'{col_name}{year}')
            elif col_name == 'overTimeGoals':
                overTimeGoals.append(f'{col_name}{year}')
            elif col_name == 'pim':
                pim.append(f'{col_name}{year}')
            elif col_name == 'games':
                games.append(f'{col_name}{year}')
            elif col_name == 'timeOnIce':
                timeOnIce.append(f'{col_name}{year}')
            else:
                shots.append(f'{col_name}{year}')

    col_filters = [shortHandedPoints,
                    powerPlayGoals,
                    powerPlayTimeOnIcePerGame,
                    shortHandedTimeOnIce,
                    shortHandedGoals,
                    evenTimeOnIce,
                    shortHandedTimeOnIcePerGame,
                    penaltyMinutes,
                    gameWinningGoals,
                    timeOnIcePerGame,
                    assists,
                    blocked,
                    points,
                    hits,
                    shifts,
                    powerPlayTimeOnIce,
                    plusMinus,
                    powerPlayPoints,
                    evenTimeOnIcePerGame,
                    goals,
                    overTimeGoals,
                    pim,
                    games,
                    timeOnIce,
                    shots,]

    for filter in col_filters:
        temp_df = df[filter]
        df[f'career_{filter[0]}'] = temp_df.sum(axis=1)
    
    return df

