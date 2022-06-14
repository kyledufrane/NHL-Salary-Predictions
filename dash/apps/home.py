from dataclasses import dataclass
from dash import html, dash_table, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from operator import itemgetter

from app import app

# --------------------------- Column Filters ------------------------------------------------------

dropped_columns = [
   'birthDate',
   'nationality',
   'id',
   'jerseyNumber',
   'code',
   'type', 
   'abbreviation',
   'birthStateProvince',
   'Team_Number',
   'Unnamed: 0',
   'index',
   'alternateCaptain',
   'captain',
   'active',
   'rookie',
   'rosterStatus',
   'birthCity'
]

basic_player = ['Salary_Rank',
                'fullName',
                'Salary_2021-22',
                'name',
                'currentAge',
                'height',
                'weight',
                'shootsCatches',
                'birthCountry'
]
offense = [
     'fullName',
     'Salary_Rank',
     'Salary_2021-22',
     'name',
     'assists22',
     'goals22',
     'shots22',
     'faceOffPct22',
     'shotPct22',
     'gameWinningGoals22',
     'overTimeGoals22',
     'points22',
     'plusMinus22',
]
special_teams = [
     'fullName',
     'Salary_2021-22',
     'Salary_Rank',
     'name',
     'powerPlayGoals22',
     'powerPlayPoints22',
     'powerPlayTimeOnIce22',
     'shortHandedGoals22',
     'shortHandedPoints22',
     'shortHandedTimeOnIce22',
]
enforcer = [
     'fullName',
     'Salary_2021-22',
     'Salary_Rank',
     'name',
     'hits22',
     'penaltyMinutes22',
]
endurance = [
         'fullName',
         'Salary_2021-22',
         'Salary_Rank',
         'name',
         'timeOnIce22',
         'games22',
         'shifts22',
         'blocked22',
         'timeOnIcePerGame22',
         'evenTimeOnIcePerGame22',
         'shortHandedTimeOnIcePerGame22',
         'powerPlayTimeOnIcePerGame22',
]

# --------------------------- Base DataFrame -------------------------------------------------

df = pd.read_csv('~/Desktop/NHL-Salary-Predictions/data/cleaned_player_df_dash.csv').drop(dropped_columns, axis=1)
df['shootsCatches'] = df['shootsCatches'].replace('L', 'Left').replace('R', 'Right')
df['Salary_Rank'] = df['Salary_2021-22'].rank(method='first', ascending=False)
df = df[df['Salary_2021-22'] != 0.0]
df['id'] = df['fullName']
df.set_index('id', inplace=True, drop=False)

active_cell = {'row': 0, 'column': 1, 'column_id': 'Player Name', 'row_id': 0}

# --------------------------- Inital Data Table DataFrame -------------------------------------
active_cell = {'row': 0, 'column': 1, 'column_id': 'Player Name', 'row_id': 0}

basic_player_data = df[basic_player].sort_values('Salary_2021-22', ascending=False)

# Dash Formatting
money = dash_table.FormatTemplate.money(2)

basic_player_columns = [
    dict(id='Salary_Rank',
         name='Salary Rank',
         type='numeric'),
    dict(id='fullName', 
         name='Player Name'),
    dict(id='Salary_2021-22',
         name='Salary',
         type='numeric',
         format=money),
    dict(id='name', 
         name='Position'),
    dict(id='currentAge',
         name='Age'),
    dict(id='height',
         name='Height',
         type='any'),
    dict(id='weight',
         name='Weight'),
    dict(id='shootsCatches',
         name='Shoots'),
    dict(id='birthCountry',
         name='Nationality')
]

# --------------------------- Offensive Stat's -------------------------------------------------

offense_data = df[offense].copy()

# Dash Formatting
offensive_columns = [
     dict(id='fullName', name='Player Name'),
     dict(id='Salary_2021-22',
          name='Salary',
          type='numeric',
          format=money),
     dict(id='Salary_Rank',
          name='Salary Rank',
          type='numeric'),
     dict(id='overall_rank',
          name='Player Rank',
          type='numeric'),
     dict(id='name',
          name='Position'),
     dict(id='assists22',
          name='Total Assists',
          type='numeric'),
     dict(id='goals22',
          name='Total Goals',
          type='numeric'),
     dict(id='shots22',
          name='Total Shots',
          type='numeric'),
     dict(id='faceOffPct22',
          name='Face Off Percentage',
          type='numeric',
          format=dash_table.Format.Format(precision=2,
                                          scheme=dash_table.Format.Scheme.percentage)),
     dict(id='shotPct22',
          name='Shot Percentage',
          type='numeric',
          format=dash_table.Format.Format(precision=2,
                                          scheme=dash_table.Format.Scheme.percentage)),
     dict(id='gameWinningGoals22',
          name='Game Winning Goals',
          type='numeric'),
     dict(id='overTimeGoals22',
          name='Over Time Goals',
          type='numeric'),
     dict(id='points22',
          name='Points',
          type='numeric'),
     dict(id='plusMinus22',
          name='Plus Minus',
          type='numeric')
]

# --------------------------- Special Team Stat's ----------------------------------------------

special_team_data = df[special_teams].copy()
special_team_data['powerPlayTimeOnIce22'] = special_team_data['powerPlayTimeOnIce22'].str.replace(':', '.').astype(float)
special_team_data['shortHandedTimeOnIce22'] = special_team_data['shortHandedTimeOnIce22'].str.replace(':', '.').astype(float)

# Dash Formatting
special_teams_columns = [
     dict(id='fullName',
          name='Player Name'),
     dict(id='Salary_2021-22',
          name='Salary',
          type='numeric',
          format=money),
     dict(id='Salary_Rank',
          name='Salary Rank',
          type='numeric'),
     dict(id='overall_rank',
          name='Player Rank',
          type='numeric'),
     dict(id='name',
          name='Position'),
     dict(id='powerPlayGoals22',
          name='Power Play Goals', 
          type='numeric'),
     dict(id='powerPlayPoints22',
          name='Power Play Points',
          type='numeric'),
     dict(id='powerPlayTimeOnIce22',
          name='Power Play Time On Ice',
          type='numeric',
          format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),
     dict(id='shortHandedGoals22',
          name='Short Handed Goals',
          type='numeric'),
     dict(id='shortHandedPoints22',
          name='Short Handed Points',
          type='numeric'),
     dict(id='shortHandedTimeOnIce22',
          name='Short Handed Time On Ice', type='numeric',
          format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),
]

# --------------------------- Enforcer Stat's ----------------------------------------------

enforcer_data = df[enforcer].copy()

# Dash Formatting
enforcer_columns = [
     dict(id='fullName', name='Player Name'),
     dict(id='Salary_2021-22',
          name='Salary',
          type='numeric',
          format=money),
     dict(id='Salary_Rank',
          name='Salary Rank',
          type='numeric'),
     dict(id='overall_rank',
          name='Player Rank',
          type='numeric'),
     dict(id='name',
          name='Position'),
     dict(id='hits22', name='Total Hits',type='numeric'),
     dict(id='penaltyMinutes22', name='Total Penalty Minutes', type='numeric')
]

# --------------------------- Endurance'hits22' Stat's ----------------------------------------------

endurance_data = df[endurance].copy()

endurance_data['timeOnIce22'] = endurance_data['timeOnIce22'] \
                                        .str.replace(':', '.').astype(float)
endurance_data['timeOnIcePerGame22'] = endurance_data['timeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
endurance_data['evenTimeOnIcePerGame22'] = endurance_data['evenTimeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
endurance_data['shortHandedTimeOnIcePerGame22'] = endurance_data['shortHandedTimeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
endurance_data['powerPlayTimeOnIcePerGame22'] = endurance_data['powerPlayTimeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)

# Dash Formatting
endurance_columns = [
         dict(id='fullName', name='Player Name'),
         dict(id='Salary_2021-22',
              name='Salary 2021-22',
              type='numeric',
              format=money),
         dict(id='name',
            name='Position'),
         dict(id='timeOnIce22',
              name='Time On Ice',
              type='numeric',
              format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),
         dict(id='games22', name='Total Games', type='numeric'),
         dict(id='shifts22',name='Total Shifts', type='numeric'),
         dict(id='blocked22',name='Blocked Shots', type='numeric'),
         dict(id='timeOnIcePerGame22',
              name='Time On Ice Per Game',
              type='numeric',
              format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),              
         dict(id='evenTimeOnIcePerGame22',
              name='Even Time On Ice Per Game',
              type='numeric',
              format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),                   
         dict(id='shortHandedTimeOnIcePerGame22',
              name='Short Handed Time On Ice Per Game',
              type='numeric',
              format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),                   
         dict(id='powerPlayTimeOnIcePerGame22',
              name='Power Play Time On Ice Per Game',
              type='numeric',
              format=dash_table.Format.Format(decimal_delimiter=':').scheme('f').precision(2)),                   
]

# --------------------------- Page Layout ----------------------------------------------------

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H3(id='datatable_label',
                    className='text-center text-decoration-underline'),
            width=12)),
     dbc.Row([
          dbc.Col([
            dcc.Dropdown(options=['Basic Player Data',
                                 'Offense',
                                 'Special Teams',
                                 'Enforcer',
                                 'Endurance'
            ], 
            value='Basic Player Data', 
            id='skill_sets',
            style={'color':'black'})
        ], width=3, md=3, className='my-3'),
          dbc.Col([
            dcc.Dropdown(options=['All Positions',
                                  'Center',
                                  'Right Wing',
                                  'Left Wing',
                                  'Defenseman'],
                        value='All Positions',
                        id='position',
                        style={'color':'black'})
        ], width=3, md=3, className='my-3'),
          dbc.Col([
               dcc.Dropdown(id='dataframe_feats',
                            style={'color':'black'})
          ], width=3, md=3, className='my-3'),
     ],
          justify='center'), 
     dbc.Row([
          dbc.Col(
               dash_table.DataTable(id='player_tbl',
                                 filter_action='native',
                                 sort_action="native",
                                 style_cell={'textAlign': 'left'},
                                 style_as_list_view=True,
                                 style_data={'color': 'black',
                                             'backgroundColor': 'white',
                                             'border': '1px solid black'},
                                 style_header={'backgroundColor': 'white',
                                               'color': 'black',
                                               'fontWeight': 'bold',
                                               'border': '1px solid black'},
                                 style_table={'overflowX':'scroll',
                                              'overflowY': 'scroll',
                                              'height': '750px'},
                                 active_cell=active_cell,
                              #    page_size=25,
                                 ), className='my-3', 
                                 width={'size':5}),
          dbc.Col(dcc.Graph(id='player_graph'), width={'size':5}, className='my-3')
     ], justify='center'),
     ], fluid=True)

@app.callback(
    [Output('player_tbl', 'data'),
     Output('player_tbl', 'columns'),
     Output('datatable_label', 'children'),
     Output('dataframe_feats', 'options'),
     Output('dataframe_feats', 'value')],
    [Input('skill_sets', 'value'),
     Input('position', 'value')])
def update_datatable(skills_sets_dropdown, position_dropdown):
    if skills_sets_dropdown == 'Basic Player Data':
        df = basic_player_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = basic_player_columns
        label_ = [f"{position_dropdown} Basic Player Data"]
    
    elif skills_sets_dropdown == 'Offense':
        df = offense_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = offensive_columns
        label_ = [f"{position_dropdown} Offensive Player Data"]

    elif skills_sets_dropdown == 'Special Teams':
        df = special_team_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = special_teams_columns    
        label_ = [f"{position_dropdown} Special Teams Data"]
     
    elif skills_sets_dropdown == 'Endurance':
       df = endurance_data.copy()
       if position_dropdown != 'All Positions':
          df = df[df['name'] == position_dropdown].copy()
       else:
          df
       columns = endurance_columns
       label_ = [f"{position_dropdown} Endurance Data"]

    else:
        df = enforcer_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = enforcer_columns
        label_ = [f"{position_dropdown} Enforcer Data"]

    # Formatting for % in data table and creating quantiles
    for col in df.columns:
        if 'Pct' in col:
            df[col] = df[col]/100
        if df[col].dtype != 'object':
            df[f'{col}_quantile'] = pd.qcut(df[col].rank(method='first'),5,labels=False).copy()
    # Ranking players
    columns_ = []

    for col in df.columns:
        if 'quantile' in col:
            columns_.append(col)

    df['sum_quantiles'] = df[columns_].sum(axis=1)
    df['overall_rank'] = df['sum_quantiles'].rank(method='first', \
                                                  ascending=False).astype('int64')
    df = df.sort_values('overall_rank', ascending=False)
    removed_cols = ['rank', 'Salary']
    feats_dropdown = sorted([
                    col['name'] for col in columns \
                         if col['id'] in df.select_dtypes(['float64', 'int64']).columns \
                              if not any(unwanted_cols in col['id'] for unwanted_cols in removed_cols)
    ])

    if skills_sets_dropdown == 'Basic Player Data':
     df = df
    
    elif skills_sets_dropdown == 'Offense':
          new_cols = ['Salary_Rank', 
                    'overall_rank', 
                    'fullName',
                    'Salary_2021-22',
                    'name',
                    'assists22',
                    'goals22',
                    'shots22',
                    'faceOffPct22',
                    'shotPct22',
                    'gameWinningGoals22',
                    'overTimeGoals22',
                    'points22',
                    'plusMinus22',]

    elif skills_sets_dropdown == 'Special Teams':
     df = df[['Salary_Rank', 
               'overall_rank',     
               'fullName',
               'Salary_2021-22',
               'name',
               'powerPlayGoals22',
               'powerPlayPoints22',
               'powerPlayTimeOnIce22',
               'shortHandedGoals22',
               'shortHandedPoints22',
               'shortHandedTimeOnIce22', ]]
    
    elif skills_sets_dropdown == 'Endurance':
     df = df[['Salary_Rank', 
               'overall_rank',
               'fullName',
               'Salary_2021-22'
               'name',
               'timeOnIce22',
               'games22',
               'shifts22',
               'blocked22',
               'timeOnIcePerGame22',
               'evenTimeOnIcePerGame22',
               'shortHandedTimeOnIcePerGame22',
               'powerPlayTimeOnIcePerGame22',]]
     
    else:
     df = df[['Salary_Rank', 
               'overall_rank',
               'fullName',
               'Salary_2021-22',
               'name',
               'hits22',
               'penaltyMinutes22',]]

    return df.to_dict('records'), \
           columns, \
           label_, \
           feats_dropdown, \
           feats_dropdown[0], \

@app.callback(
     [Output('player_graph', 'figure')],
     [Input('player_tbl', 'data'),
      Input('player_tbl', 'columns'),
      Input('dataframe_feats', 'value'),
      Input('skill_sets', 'value'),
      Input('position', 'value')]
)
def update_graph(data,
                columns,
                feature, 
                skill_sets_dropdown, 
                position_dropdown):
    data_ = pd.DataFrame(data)

    col_name = [
          col['id'] for col in columns \
               if feature == col['name']
    ][0]
    x_axis_label = [
          col['name'] for col in columns \
               if feature == col['name']
    ][0]

    data_label_ = np.full_like(data_['fullName'], str(x_axis_label))
    custom_data = np.stack((data_['overall_rank'], data_['Salary_Rank'], data_label_),axis=-1)

    hover_template = "<b>Player Name: </b> %{text} <br><br>"
    hover_template += "<b>%{customdata[2]}: </b> %{x} <br>"
    hover_template += "<b>Salary: </b> $%{y} <br>"
    hover_template += "<b>Salary Rank: </b> %{customdata[1]} <br>"
    hover_template += "<b>Player Rank: </b> %{customdata[0]}"

    fig = go.Figure(go.Scatter(
                        x=data_[str(col_name)],
                        y=data_['Salary_2021-22'],
                        mode='markers',
                        text=data_['fullName'],
                        customdata=custom_data,
                        hovertemplate=hover_template,
                        showlegend=False,
                        name='playerName',
                        ))

    fig.update_layout(title={'text': f"<em>Group:</em>{skill_sets_dropdown} <em>Position:</em>{position_dropdown} <em>Data:</em>{feature}",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                      xaxis_title=f"{x_axis_label}",
                      yaxis_title="Player Salaries 2021-22")

#     fig.add_trace(go.Scatter(x=np.array(data_.iloc[active_cell['row']][col_name]), \
#                     y=np.array(data_.iloc[active_cell['row']]['Salary_2021-22']),
                    
#                     marker_symbol='star',
#                     marker_size=15,
#                     showlegend=False))
#     print(filtered_data)

    return [fig]
