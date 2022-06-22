from dash import html, dash_table, Input, Output, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from app import app

height = []
for feet in [5,6]:
    for inches in range(1,12):
        height.append(f"{feet}\'{inches}\"")

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
                        html.H4('Current Age',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dbc.Input(
                            type='number',
                            min=16,
                            max=50,
                            step=1,
                            value=25,
                            className=className_,
                            style=style_,
                            id='currentage'
                        ),
                        html.H4('Height',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dcc.Dropdown(
                            options=height,
                            value=height[5],
                            className=className_,
                            id='height'
                        ),
                        html.H4('Weight',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dbc.Input(
                            type='number',
                            min=100,
                            max=300,
                            step=1,
                            value=200,
                            style=style_,
                            className=className_,
                            id='weight'
                        )            
                    ],
                    width=3,
                    ),
                    dbc.Col([
                        html.H4('Position',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dcc.Dropdown(
                            options=[
                                'Center',
                                'Right Wing',
                                'Left Wing',
                                'Defensean'
                            ],
                            value='Center',
                            className=className_,
                            id='position'
                        ),
                        html.H4('Shot',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dcc.Dropdown(
                            options=[
                                'Left',
                                'Right'
                            ],
                            value='Right',
                            className=className_,
                            id='shot'
                        ),
                        html.H4('Birth Country',
                                style={
                                    'textAlign':'center',
                                    'text-decoration':'underline'
                                },
                                className='py-3'
                        ),
                        dcc.Dropdown(
                            options=[
                                'CAN',
                                'USA'
                            ],
                            value='CAN',
                            className=className_,
                            id='birthcountry'
                        ) 
                    ],
                    width=3,
                    style={'margin-left':'25px'}
                    )],
                justify='center',
                )
            ]),
        dcc.Tab(label='Advanced Salary Prediction')
    ]
)

@app.callback(
    [
        Output('basic_predicted_salary', 'children')
    ],
    [
        Input('currentage', 'value'),
        Input('height', 'value'),
        Input('weight', 'value'),
        Input('position', 'value'),
        Input('shot', 'value'),
        Input('birthcountry', 'value')
    ]
)
def get_basic_prediction(age, height, weight, position, shot, birthcountry):
    print(age, height, weight, position, shot, birthcountry)
    return [birthcountry]