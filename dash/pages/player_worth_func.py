from dash import html, dcc
import dash_bootstrap_components as dbc

import pandas as pd


def clean_data():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/kyledufrane/NHL-Salary-Predictions/main/data/ml_cleaned_forward_players_df.csv')

    drop = [
        'birthCity',
        'birthDate',
        'Unnamed: 0',
        'index',
        'birthStateProvince',
        'height'
    ]

    df.drop(drop, axis=1, inplace=True)
    for col in df.select_dtypes(['int64', 'float64']).columns:
        mean_ = df[col].mean()
        df[col].fillna(mean_, inplace=True)

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
                   shots, ]

    for filter in col_filters:
        temp_df = df[filter]
        df[f'career_{filter[0][:-2]}'] = temp_df.sum(axis=1)

    return df


def add_header(header):
    return html.H4(
        header,
        style={
            'textAlign': 'center',
            'text-decoration': 'underline'
        },
        className='py-3'
    )


def add_slider_input(df, data):
    return dbc.Row([
        dbc.Col(
            dcc.Slider(
                id=f'{data}_slider',
                min=0,
                max=df[data].max() * 1.25,
                value=round(df[data].mean()),
                step=1,
                marks=None,
                className='my-2'
            ),
            style={
                'textAlign': 'left'
            }
        ),
        dbc.Col(
            dcc.Input(
                id=f"{data}_input",
                type='number',
                value=round(df[data].mean()),
                style={
                    'width': '50%'
                }
            ),
        )
    ])


def convert_dash_format(layout):
    convert = ()
    for i in range(len(layout)):
        convert += layout[i]
    return convert


def slider_input_update(slider_val, input_val, old_slider_val, old_input_val):
    if slider_val != input_val:
        if slider_val == old_slider_val:
            updated_slider_val = input_val
            updated_input_val = input_val
        else:
            updated_input_val = slider_val
            updated_slider_val = slider_val
        return updated_slider_val, updated_input_val


def check_for_update(slider, input_, slider_output, input_output):
    if slider != input_:
        slider_updated, input_updated = slider_input_update(
            slider, input_, slider_output, input_output)
    else:
        slider_updated = slider
        input_updated = input_
    return slider_updated, input_updated
