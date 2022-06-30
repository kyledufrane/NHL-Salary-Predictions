import sys

from pyrsistent import m
sys.path.append('/home/kyle/Desktop/NHL-Salary-Predictions')
from src.home_func import *
from distutils.command.build import build
from dash import html, dash_table, Input, Output, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from app import app

from home_func import *

# --------------------------- External Variables ----------------------------------------------------

# Initial cell selected in data table
active_cell = {'row': 6, 'column': 3,
               'column_id': 'fullName', 'row_id': 'None'}

# --------------------------- Page Layout ----------------------------------------------------

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Input(
                id='player_search',
                type='search',
                placeholder='Enter Player Name',
                className='border border-primary'
            ),
            width=4,
            className='my-3'
        ),
        dbc.Col(
            dcc.Dropdown(
                options=[
                    'Basic Player Data',
                    'Offense',
                    'Special Teams',
                    'Enforcer',
                    'Endurance'
                ],
                value='Basic Player Data',
                id='skill_set_dropdown',
                style={
                    'color': 'black',
                    'height': '47px',
                    'textAlign': 'center'
                },
                className='border border-primary'
            ),
            width=3,
            className='my-3'
        ),
        dbc.Col(
            dcc.Dropdown(
                options=[
                    'All Positions',
                    'Center',
                    'Right Wing',
                    'Left Wing',
                    'Defenseman'
                ],
                value='All Positions',
                id='position_dropdown',
                style={
                    'color': 'black',
                    'height': '47px',
                    'textAlign':'center',
                    'verticalAlign': 'middle'
                },
                className='border border-primary'
            ),
            width=3,
            className='my-3'
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                active_cell=active_cell,
                style_cell={'textAlign': 'left'},
                style_data={'color': 'blue',
                            'backgroundColor': 'white',
                            'border': 'none'},
                style_header={'display': 'none'},
                style_table={'overflowX': 'scroll',
                             'overflowY': 'scroll',
                             'height': '750px'},
                id='player_tbl'
            ),
            width=2
        ),
        dbc.Col([
            dcc.Dropdown(
                id='dataframe_features_dropdown',
                style={'color': 'black',
                       'textAlign': 'center'},
                className='border border-primary'
            ),
            dcc.Graph(
                id='player_kde'
            ),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        daq.LEDDisplay(
                            label='Salary Rank',
                            id='salary_rank'),
                        daq.LEDDisplay(
                            label='Overall Rank',
                            id='overall_rank',
                        ),
                    ]),
                    dbc.Col([
                        daq.LEDDisplay(
                            label='Offensive_Rank',
                            id='offensive_rank'),
                        daq.LEDDisplay(
                            label='Special Teams Rank',
                            id='special_teams_rank'),
                    ]),
                    dbc.Col([
                        daq.LEDDisplay(
                            label='Enforcer Rank',
                            id='enforcer_rank'),
                        daq.LEDDisplay(
                            label='Endurance Rank',
                            id='endurance_rank'),
                    ])
                ])
            ])
        ],
            width=10
        ),
        dbc.Row(
            html.H2(
                id='player_name',
                style={'textAlign': 'center'}
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Hr(
                    style={
                        'color': 'black',
                        'height': '5px',
                        'opacity': '100'
                    }
                ),
                width=10,
            ),
            justify='center'
        ),
        dbc.Row([
            dbc.Col(
                id='stats_description',
                width='auto',
                className='my-4',
            ),
            dbc.Col(
                id='stats_values',
                width=3,
                className='my-4',
            )],
            justify='center'
        )
    ])],
    fluid=True
)


@app.callback(
    [
        Output('player_tbl', 'data'),
        Output('player_tbl', 'columns'),
        Output('dataframe_features_dropdown', 'options'),
        Output('dataframe_features_dropdown', 'value'),
        Output('player_name', 'children'),
        Output('stats_description', 'children'),
        Output('stats_values', 'children'),
        Output('salary_rank', 'value'),
        Output('overall_rank', 'value'),
        Output('offensive_rank', 'value'),
        Output('special_teams_rank', 'value'),
        Output('enforcer_rank', 'value'),
        Output('endurance_rank', 'value'),
        Output('player_kde', 'figure')
    ],
    [
        Input('skill_set_dropdown', 'value'),
        Input('position_dropdown', 'value'),
        Input('dataframe_features_dropdown', 'value'),
        Input('player_kde', 'selectedData'),
        Input('player_kde', 'relayoutData'),
        Input('player_tbl', 'active_cell'),
        Input('player_search', 'value'),
    ]
)
def update_page(skill_sets_dropdown, position_dropdown, dataframe_features_dropdown, kde_selected_data, kde_relayout_data, player_tbl_active_cell, player_search):

    columns = [dict(id='Player Name', name='Player Name')]

    df_ = filter_data(skill_sets_dropdown, position_dropdown)

    # Filter and sort column descriptions for dataframe features dropdown
    wanted_columns = select_columns(df_, skill_sets_dropdown)

    # Selecting features dropdown initial value
    if dataframe_features_dropdown is not None:
        if dataframe_features_dropdown == wanted_columns[0]:
            dataframe_features_dropdown_value = wanted_columns[0]
        elif dataframe_features_dropdown not in wanted_columns:
            dataframe_features_dropdown_value = wanted_columns[0]
        else:
            dataframe_features_dropdown_value = dataframe_features_dropdown
    else:
        dataframe_features_dropdown_value = wanted_columns[0]

    # filtering dataframe based on selected points
    if kde_selected_data != None:
        try:
            feature_ = kde_selected_data['points'][0]['y']
            value_ = kde_selected_data['points'][0]['x']
            if feature_ in wanted_columns:
                if feature_ == 'Height':
                    df_ = df_[df_['Height (Inches)'] == value_]
                else:
                    df_ = df_[df_[feature_] == value_]
        except:
            pass

    # Filtering based on user selected data
    if len(kde_relayout_data) > 1 and 'xaxis.autorange' not in kde_relayout_data.keys():
        dropdown_values = [skill_sets_dropdown,
                           position_dropdown, dataframe_features_dropdown]
        if dataframe_features_dropdown_value == 'Height':
            df_ = df_[(df_['Height (Inches)'] >= kde_relayout_data['xaxis.range[0]'])
                      & (df_['Height (Inches)'] <= kde_relayout_data['xaxis.range[1]'])]
        else:
            df_ = df_[(df_[dataframe_features_dropdown_value] >= kde_relayout_data['xaxis.range[0]'])
                      & (df_[dataframe_features_dropdown_value] <= kde_relayout_data['xaxis.range[1]'])]

    # Selecting player name for display
    player_name = player_tbl_active_cell['row_id']
    if player_name == 'None':
        player_name = 'Please Select A Player To View Their Stats'
    else:
        player_name

    # Grabbing player stats for display
    stats_descriptions = [
        html.H3(children=col, style={'textAlign': 'center'})
        for col in wanted_columns
    ]

    data_label_ = np.full_like(
        df_['Player Name'], dataframe_features_dropdown_value)

    customdata = np.stack((df_['Player Name'], df_['Overall Rank'], df_[
                          'Salary Rank'], data_label_), axis=-1)

    hover_template = "<b>Player Name: </b> %{customdata[0]} <br><br>"
    hover_template += "<b>%{customdata[3]}: </b> %{x} <br>"
    hover_template += "<b>Salary Rank: </b> %{customdata[2]} <br>"
    hover_template += "<b>Player Rank: </b> %{customdata[1]}"

    if player_name != 'Please Select A Player To View Their Stats':

        df_name = df_[df_['Player Name'] == player_name]

        for col in df_name.columns:
            if 'Time' in col and 'quantile' not in col and 'Goals' not in col:
                df_name[col] = df_name[col].astype(
                    str).str.replace('.', ':') + ' Min'
            if 'Percentage' in col:
                df_name[col] = round((df_name[col]*100), 2).astype(str) + '%'

        stats_values = [
            html.H3(children=df_name[val], style={'textAlign': 'center'})
            for val in wanted_columns
        ]

        salary_rank = df_name['Salary Rank']
        overall_rank = df_name['Overall Rank']
        offensive_rank = df_name['Offensive Overall Rank']
        special_teams_rank = df_name['Special Teams Overall Rank']
        enforcer_rank = df_name['Enforcer Overall Rank']
        endurance_rank = df_name['Endurance Overall Rank']

        try:
            if dataframe_features_dropdown == 'Height' and 'Height' in wanted_columns:
                fig = build_plot(dataframe_features_dropdown_value,
                                 df_, 'Height (Inches)', hover_template, customdata)
                try:
                    fig.add_vline(x=np.array(df_[df_['Player Name'] == player_name]['Height (Inches)'])[
                                  0], line_color='yellow')
                except:
                    player_name,  \
                    stats_values,  \
                    salary_rank,  \
                    overall_rank,  \
                    offensive_rank, \
                    special_teams_rank, \
                    enforcer_rank, \
                    endurance_rank = return_default_values(wanted_columns)

            else:
                fig = build_plot(dataframe_features_dropdown_value, df_,
                                 dataframe_features_dropdown_value, hover_template, customdata)
                try:
                    fig.add_vline(x=np.array(df_[df_['Player Name'] == player_name][dataframe_features_dropdown_value])[
                                  0], line_color='yellow')
                except:
                    player_name,  \
                    stats_values,  \
                    salary_rank,  \
                    overall_rank,  \
                    offensive_rank, \
                    special_teams_rank, \
                    enforcer_rank, \
                    endurance_rank = return_default_values(wanted_columns)

        except:
            fig = {}
    else:
        player_name,  \
        stats_values,  \
        salary_rank,  \
        overall_rank,  \
        offensive_rank, \
        special_teams_rank, \
        enforcer_rank, \
        endurance_rank = return_default_values(wanted_columns)
        fig = {}

    # Filtering from search bar
    if player_search != None:
        df_ = df_[df_['Player Name'].str.contains(player_search)]

    return df_.to_dict('records'), \
        columns, \
        wanted_columns, \
        dataframe_features_dropdown_value, \
        player_name, \
        stats_descriptions, \
        stats_values, \
        salary_rank, \
        overall_rank, \
        offensive_rank, \
        special_teams_rank, \
        enforcer_rank, \
        endurance_rank, \
        fig
