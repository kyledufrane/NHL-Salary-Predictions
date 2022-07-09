from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import pickle

from app import app

from .player_worth_func import *

df = clean_data()

with open('model/rf_10_feats', 'rb') as f:
    clf = pickle.load(f)

first_pass = True
career_assists_slider_output = int()
career_assists_input_output = int()
career_points_slider_output = int()
career_points_input_output = int()
career_shots_slider_output = int()
career_shots_input_output = int()
career_timeOnIce_slider_output = int()
career_timeOnIce_input_output = int()
career_evenTimeOnIce_slider_output = int()
career_evenTimeOnIce_input_output = int()
career_powerPlayTimeOnIcePerGame_slider_output = int()
career_powerPlayTimeOnIcePerGame_input_output = int()
career_powerPlayTimeOnIce_slider_output = int()
career_powerPlayTimeOnIce_input_output = int()
career_powerPlayPoints_slider_output = int()
career_powerPlayPoints_input_output = int()
powerPlayTimeOnIcePerGame22_slider_output = int()
powerPlayTimeOnIcePerGame22_input_output = int()
assists22_slider_output = int()
assists22_input_output = int()

column_one_map = {
    'Career Assists': 'career_assists',
    'Career Points': 'career_points',
    'Career Shots': 'career_shots',
    'Career TOI': 'career_timeOnIce',
    'Career Even TOI': 'career_evenTimeOnIce'
}

column_two_map = {
    'Career PP TOI PG': 'career_powerPlayTimeOnIcePerGame',
    'Career PP TOI': 'career_powerPlayTimeOnIce',
    'Career PP Points': 'career_powerPlayPoints',
    'PP TOI PG 2021-22': 'powerPlayTimeOnIcePerGame22',
    'Total Assists 2021-22': 'assists22'
}

column_one_layout = convert_dash_format([
    (add_header(header),
     add_slider_input(df, data))
    for header, data in column_one_map.items()
])

column_two_layout = convert_dash_format([
    (add_header(header),
     add_slider_input(df, data))
    for header, data in column_two_map.items()
])

layout = dbc.Container([
    dbc.Row(
        html.H2(
            'Your Predicted Salary Is:',
            style={
                'textAlign': 'center'
            }),
        className='my-5'
    ),
    dbc.Row(
        html.H1(
            id='basic_predicted_salary',
            style={
                'textAlign': 'center'
            }),
        className='my-5'
    ),
    dbc.Row(
        dbc.Col(
            html.Hr(
                style={
                    'color': 'black',
                    'height': '5px',
                    'opacity': '100',
                }
            ),
            width=10,
        ),
        justify='center',
    ),
    dbc.Row([
        dbc.Col(
            column_one_layout,
            width=5,
        ),
        dbc.Col(
            column_two_layout,
            width=5,
        )
    ],
        justify='center',
    ),
    dbc.Row(
        dbc.Col([
            dbc.Row(
                html.H4(
                    'Legend',
                    style={
                        'textAlign': 'center',
                        'text-decoration': 'underline'
                    }
                ),
            ),
            dbc.Row(
                html.H5(
                    'PP: Power Play'
                )
            ),
            dbc.Row(
                html.H5(
                    'TOI: Time On Ice'
                )
            ),
            dbc.Row(
                html.H5(
                    'PG: Per Game'
                )
            )
        ],
            style={
                'textAlign': 'center',
                'border': '2px black solid'
            },
            className='my-5'
        )
    )
])

all_columns = {**column_one_map, **column_two_map}

callback_outputs = [
    (Output(f'{data}_slider', 'value'),
     Output(f'{data}_input', 'value'))
    for data in all_columns.values()
]

callback_outputs = convert_dash_format(callback_outputs)

prediction = Output('basic_predicted_salary', 'children')
callback_outputs = list((*callback_outputs, prediction))

callback_inputs = [
    (Input(f'{data}_slider', 'value'),
     Input(f'{data}_input', 'value'))
    for data in all_columns.values()
]

callback_inputs = list(convert_dash_format(callback_inputs))


@app.callback(
    callback_outputs,
    callback_inputs
)
def basic_pred(career_assists_slider, career_assists_input, career_points_slider, career_points_input,
               career_shots_slider, career_shots_input, career_timeOnIce_slider, career_timeOnIce_input,
               career_evenTimeOnIce_slider, career_evenTimeOnIce_input, career_powerPlayTimeOnIcePerGame_slider,
               career_powerPlayTimeOnIcePerGame_input, career_powerPlayTimeOnIce_slider,
               career_powerPlayTimeOnIce_input, career_powerPlayPoints_slider,
               career_powerPlayPoints_input, powerPlayTimeOnIcePerGame22_slider,
               powerPlayTimeOnIcePerGame22_input, assists22_slider, assists22_input):
    global first_pass, \
        career_assists_slider_output, \
        career_assists_input_output, \
        career_points_slider_output, \
        career_points_input_output, \
        career_shots_slider_output, \
        career_shots_input_output, \
        career_timeOnIce_slider_output, \
        career_timeOnIce_input_output, \
        career_evenTimeOnIce_slider_output, \
        career_evenTimeOnIce_input_output, \
        career_powerPlayTimeOnIcePerGame_slider_output, \
        career_powerPlayTimeOnIcePerGame_input_output, \
        career_powerPlayTimeOnIce_slider_output, \
        career_powerPlayTimeOnIce_input_output, \
        career_powerPlayPoints_slider_output, \
        career_powerPlayPoints_input_output, \
        powerPlayTimeOnIcePerGame22_slider_output, \
        powerPlayTimeOnIcePerGame22_input_output, \
        assists22_slider_output, \
        assists22_input_output

    if first_pass:
        first_pass = False
        career_assists_slider_output = career_assists_slider
        career_assists_input_output = career_assists_input
        career_points_slider_output = career_points_slider
        career_points_input_output = career_points_input
        career_shots_slider_output = career_shots_slider
        career_shots_input_output = career_shots_input
        career_timeOnIce_slider_output = career_timeOnIce_slider
        career_timeOnIce_input_output = career_timeOnIce_input
        career_evenTimeOnIce_slider_output = career_evenTimeOnIce_slider
        career_evenTimeOnIce_input_output = career_evenTimeOnIce_input
        career_powerPlayTimeOnIcePerGame_slider_output = career_powerPlayTimeOnIcePerGame_slider
        career_powerPlayTimeOnIcePerGame_input_output = career_powerPlayTimeOnIcePerGame_input
        career_powerPlayTimeOnIce_slider_output = career_powerPlayTimeOnIce_slider
        career_powerPlayTimeOnIce_input_output = career_powerPlayTimeOnIce_input
        career_powerPlayPoints_slider_output = career_powerPlayPoints_slider
        career_powerPlayPoints_input_output = career_powerPlayPoints_input
        powerPlayTimeOnIcePerGame22_slider_output = powerPlayTimeOnIcePerGame22_slider
        powerPlayTimeOnIcePerGame22_input_output = powerPlayTimeOnIcePerGame22_input
        assists22_slider_output = assists22_slider
        assists22_input_output = assists22_input

    career_assists_slider_output, career_assists_input_output = check_for_update(
        career_assists_slider, career_assists_input, career_assists_slider_output, career_assists_input_output)
    career_points_slider_output, career_points_input_output = check_for_update(
        career_points_slider, career_points_input, career_points_slider_output, career_points_input_output)
    career_shots_slider_output, career_shots_input_output = check_for_update(
        career_shots_slider, career_shots_input, career_shots_slider_output, career_shots_input_output)
    career_timeOnIce_slider_output, career_timeOnIce_input_output = check_for_update(
        career_timeOnIce_slider, career_timeOnIce_input, career_timeOnIce_slider_output, career_timeOnIce_input_output)
    career_evenTimeOnIce_slider_output, career_evenTimeOnIce_input_output = check_for_update(
        career_evenTimeOnIce_slider, career_evenTimeOnIce_input, career_evenTimeOnIce_slider_output,
        career_evenTimeOnIce_input_output)
    career_powerPlayTimeOnIcePerGame_slider_output, career_powerPlayTimeOnIcePerGame_input_output = check_for_update(
        career_powerPlayTimeOnIcePerGame_slider, career_powerPlayTimeOnIcePerGame_input,
        career_powerPlayTimeOnIcePerGame_slider_output, career_powerPlayTimeOnIcePerGame_input_output)
    career_powerPlayTimeOnIce_slider_output, career_powerPlayTimeOnIce_input_output = check_for_update(
        career_powerPlayTimeOnIce_slider, career_powerPlayTimeOnIce_input, career_powerPlayTimeOnIce_slider_output,
        career_powerPlayTimeOnIce_input_output)
    career_powerPlayPoints_slider_output, career_powerPlayPoints_input_output = check_for_update(
        career_powerPlayPoints_slider, career_powerPlayPoints_input, career_powerPlayPoints_slider_output,
        career_powerPlayPoints_input_output)
    powerPlayTimeOnIcePerGame22_slider_output, powerPlayTimeOnIcePerGame22_input_output = check_for_update(
        powerPlayTimeOnIcePerGame22_slider, powerPlayTimeOnIcePerGame22_input,
        powerPlayTimeOnIcePerGame22_slider_output, powerPlayTimeOnIcePerGame22_input_output)
    assists22_slider_output, assists22_input_output = check_for_update(
        assists22_slider, assists22_input, assists22_slider_output, assists22_input_output)

    data_map = {
        'career_assists': career_assists_slider_output,
        'career_points': career_points_slider_output,
        'career_powerPlayTimeOnIcePerGame': career_powerPlayTimeOnIcePerGame_slider_output,
        'career_shots': career_shots_slider_output,
        'career_powerPlayTimeOnIce': career_powerPlayTimeOnIce_slider_output,
        'career_powerPlayPoints': career_powerPlayPoints_slider_output,
        'assists22': assists22_slider_output,
        'career_timeOnIce': career_timeOnIce_slider_output,
        'career_evenTimeOnIce': career_evenTimeOnIce_slider_output,
        'powerPlayTimeOnIcePerGame22': powerPlayTimeOnIcePerGame22_slider_output
    }

    X = pd.DataFrame.from_dict(data_map, orient='index').T

    pred = clf.predict(X)
    pred = "${:,.2f}".format(round(pred[0]))

    basic_predicted_salary_output = pred

    return career_assists_slider_output, career_assists_input_output, career_points_slider_output, \
        career_points_input_output, career_shots_slider_output, career_shots_input_output, \
        career_timeOnIce_slider_output, career_timeOnIce_input_output, career_evenTimeOnIce_slider_output, \
        career_evenTimeOnIce_input_output, career_powerPlayTimeOnIcePerGame_slider_output, \
        career_powerPlayTimeOnIcePerGame_input_output, career_powerPlayTimeOnIce_slider_output, \
        career_powerPlayTimeOnIce_input_output, career_powerPlayPoints_slider_output, \
        career_powerPlayPoints_input_output, powerPlayTimeOnIcePerGame22_slider_output, \
        powerPlayTimeOnIcePerGame22_input_output, assists22_slider_output, assists22_input_output, \
        basic_predicted_salary_output
