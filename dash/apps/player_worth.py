from dash import html, dash_table, Input, Output, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from app import app

import sys
sys.path.append('/home/kyle/Desktop/NHL-Salary-Predictions/src')
from clean_data import clean_data


df = clean_data()

style_ = {
    # 'text-align':'center',
    'height':'38px',
    'font-size': '25px',
}
className_ = "d-flex align-items-center text-center fs-4 text border border-primary mb-2"
layout = dbc.Tabs(
    id='tabs',
    children=[
        dcc.Tab(
            label='Basic Salary Prediction',
            children=[
                dbc.Row(
                    html.H2(
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
                    dbc.Col([
                        html.H4('Career Assists',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dcc.Slider(
                            id='career_assists',
                            min=0,
                            max=df['career_assists'].max() * 1.25,
                            value=round(df['career_assists'].mean()),
                            step=1,
                            marks=None,
                        ),
                        html.H4(
                            'Career Points',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='career_points',
                            min=0,
                            max=df['career_points'].max() * 1.25,
                            value=round(df['career_points'].mean()),
                            step=1,
                            marks=None
                        ),
                        html.H4(
                            'Career Shots',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='career_shots',
                            min=0,
                            max=df['career_shots'].max() * 1.25,
                            value=round(df['career_shots'].mean()),
                            step=1,
                            marks=None
                        ),
                        html.H4(
                            'Career TOI',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='career_toi',
                            min=0,
                            max=df['career_timeOnIce'].max() * 1.25,
                            value=round(df['career_timeOnIce'].mean()),
                            step=1,
                            marks=None
                        ),
                        html.H4(
                            'Career Even TOI',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='career_even_toi',
                            min=0,
                            max=df['career_evenTimeOnIce'].max() * 1.25,
                            value=round(df['career_evenTimeOnIce'].mean()),
                            step=1,
                            marks=None
                        )
                    ],
                    width=5,
                    ),
                    dbc.Col([
                        html.H4(
                            'Career PP TOI PG',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dbc.Row([
                            dbc.Col(
                                dcc.Slider(
                                    id='pp_toi_pg',
                                    min=0,
                                    max=df['career_powerPlayTimeOnIcePerGame'].max() * 1.25,
                                    value=round(df['career_powerPlayTimeOnIcePerGame'].mean()),
                                    step=1,
                                    marks=None,
                                    className='my-2'
                                ),
                            style={
                                'textAlign':'left'
                            },
                            
                            ),
                            dbc.Col(
                                dcc.Input(
                                    'id=pp_toi_pg_input',
                                    type='number',
                                    # style={
                                    #     'width':'50%'
                                    # }
                                ),
                            style={
                                'textAlign':'right'
                            },
                            width=3,
                        )]),
                        html.H4(
                            'Career PP TOI',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='career_pp_toi',
                            min=0,
                            max=df['career_powerPlayTimeOnIce'].max() * 1.25,
                            value=round(df['career_powerPlayTimeOnIce'].mean()),
                            step=1,
                            marks=None
                        ),
                        html.H4(
                            'Career PP Points',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='career_ppp',
                            min=0,
                            max=df['career_powerPlayPoints'].max() * 1.25,
                            value=round(df['career_powerPlayPoints'].mean()),
                            step=1,
                            marks=None
                        ),
                        html.H4(
                            'PP TOI PG 2021-22',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='pptoi_202122',
                            min=0,
                            max=df['powerPlayTimeOnIcePerGame22'].max() * 1.25,
                            value=round(df['powerPlayTimeOnIcePerGame22'].mean()),
                            step=1,
                            marks=None
                        ),
                        html.H4(
                            'Total Assists 2021-22',
                            style={
                                'textAlign':'center',
                                'text-decoration':'underline'
                            },
                            className='py-3'
                        ),
                        dcc.Slider(
                            id='tot_assists_202122',
                            min=0,
                            max=df['assists22'].max() * 1.25,
                            value=round(df['assists22'].mean()),
                            step=1,
                            marks=None
                        )
                    ],
                width=5,
                )],
                justify='center',
                )
            ]),
        dcc.Tab(label='Advanced Salary Prediction')
    ]
)

# @app.callback(
#     [
#         Output('basic_predicted_salary', 'children')
#     ],
#     [
#         Input('currentage', 'value'),
#         Input('height', 'value'),
#         Input('weight', 'value'),
#         Input('position', 'value'),
#         Input('shot', 'value'),
#         Input('birthcountry', 'value')
#     ]
# )
# def get_basic_prediction(age, height, weight, position, shot, birthcountry):
#     print(age, height, weight, position, shot, birthcountry)
#     return [birthcountry]