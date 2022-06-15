from dash import html, dash_table, Input, Output, callback, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
from app import app

# --------------------------- Base Column Filters ------------------------------------------------------

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


offense_base = [
     'fullName',
     'salary_rank',
     'salary_2021-22',
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
special_teams_base = [
     'fullName',
     'salary_2021-22',
     'salary_rank',
     'name',
     'powerPlayGoals22',
     'powerPlayPoints22',
     'powerPlayTimeOnIce22',
     'shortHandedGoals22',
     'shortHandedPoints22',
     'shortHandedTimeOnIce22',
]
enforcer_base = [
     'fullName',
     'salary_2021-22',
     'salary_rank',
     'name',
     'hits22',
     'penaltyMinutes22',
]
endurance_base = [
     'fullName',
     'salary_2021-22',
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

# --------------------------- DataFrame Formatting ------------------------------------------------------

filter_list = [offense_base, special_teams_base, enforcer_base, endurance_base]
filter_str = ['offense', 'special_teams', 'enforcer', 'endurance']


df = pd.read_csv('~/Desktop/NHL-Salary-Predictions/data/cleaned_player_df_dash.csv').drop(dropped_columns, axis=1)
df = df.rename(columns={'Salary_2021-22': 'salary_2021-22'})
df['shootsCatches'] = df['shootsCatches'].replace('L', 'Left').replace('R', 'Right')
df['salary_rank'] = df['salary_2021-22'].rank(method='first', ascending=False).astype('int64')
df = df[df['salary_2021-22'] != 0.0]
df['timeOnIce22'] = df['timeOnIce22'] \
                                        .str.replace(':', '.').astype(float)
df['timeOnIcePerGame22'] = df['timeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
df['evenTimeOnIcePerGame22'] = df['evenTimeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
df['shortHandedTimeOnIcePerGame22'] = df['shortHandedTimeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
df['powerPlayTimeOnIcePerGame22'] = df['powerPlayTimeOnIcePerGame22'] \
                                        .str.replace(':', '.').astype(float)
df['powerPlayTimeOnIce22'] = df['powerPlayTimeOnIce22'].str.replace(':', '.').astype(float)
df['shortHandedTimeOnIce22'] = df['shortHandedTimeOnIce22'].str.replace(':', '.').astype(float)

df['id'] = df['fullName']
df.set_index('id', inplace=True, drop=False)

# Ranking players based on category
offense_columns_ = []
special_teams_columns_ = []
enforcer_columns_ = []
endurance_columns_ = []

for idx, filter_ in enumerate(filter_list):
     dff = df[filter_].copy()
     for col in dff.columns:
          if dff[col].dtype != 'object' and 'Rank' not in col:
               dff.sort_values(f"{col}", ascending=False, inplace=True)
               df[f'{col}_quantile'] = pd.qcut(dff[col].rank(method='first'),5, duplicates='drop')
     for col_str in filter_:
          for col in df.columns:
               if 'quantile' in col and col_str in col:
                    if idx == 0:
                         offense_columns_.append(f'{col_str}_quantile')
                    elif idx == 1:
                         special_teams_columns_.append(f'{col_str}_quantile')
                    elif idx == 2:
                         enforcer_columns_.append(f'{col_str}_quantile')
                    else:
                         endurance_columns_.append(f'{col_str}_quantile')
     for filter_string in filter_str:
          if filter_string == 'offense':
               dff = df[offense_columns_]
          elif filter_string == 'special_teams':
               dff = df[special_teams_columns_]
          elif filter_string == 'enforcer':
               dff = df[enforcer_columns_]
          else:
               dff = df[endurance_columns_]
          df[f"{filter_string}_quantiles_total"] = dff.sum(axis=1)
          df.sort_values(f"{filter_string}_quantiles_total", ascending=False, inplace=True)
          df[f"{filter_string}_overall_rank"] = df[f"{filter_string}_quantiles_total"].rank(method='first').astype('int64')

overall_rank = []

for col in df.columns:
     if 'overall_rank' in col:
          overall_rank.append(col)
df['overall_rank_sum'] = df[overall_rank].sum(axis=1)
df.sort_values('overall_rank_sum', ascending=False, inplace=True)
df['overall_rank'] = df['overall_rank_sum'].rank(method='first').astype('int64')

# active_cell = {'row': 0, 'column': 1, 'column_id': 'Player Name', 'row_id': 0}

# --------------------------- Column Filters After Formatting------------------------------------------
basic_player = [
     'overall_rank',
     'salary_rank',
     'fullName',
     'salary_2021-22',
     'name',
     'currentAge',
     'height',
     'weight',
     'shootsCatches',
     'birthCountry',
     'offense_overall_rank',
     'special_teams_overall_rank',
     'enforcer_overall_rank',
     'endurance_overall_rank'
]
offense = [
     'offense_overall_rank',
     'fullName',
     'salary_rank',
     'salary_2021-22',
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
     'special_teams_overall_rank',
     'salary_rank',
     'fullName',
     'salary_2021-22',
     'name',
     'powerPlayGoals22',
     'powerPlayPoints22',
     'powerPlayTimeOnIce22',
     'shortHandedGoals22',
     'shortHandedPoints22',
     'shortHandedTimeOnIce22',
]
enforcer = [
     'enforcer_overall_rank',
     'fullName',
     'salary_2021-22',
     'salary_rank',
     'name',
     'hits22',
     'penaltyMinutes22',
]
endurance = [
     'salary_rank',
     'endurance_overall_rank',
     'fullName',
     'salary_2021-22',
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

basic_player_data = df[basic_player].sort_values('salary_2021-22', ascending=False)
offense_data = df[offense].copy()
special_team_data = df[special_teams].copy()
enforcer_data = df[enforcer].copy()
endurance_data = df[endurance].copy()


# --------------------------- Functions ----------------------------------------------------

def feet_to_float(cell_string):
    try:
        split_strings = cell_string.replace('"','').replace("'",'').split()
        float_value = (float(split_strings[0])*12)+float(split_strings[1])
    except:
        float_value = np.nan
    return float_value

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
                              #    active_cell=active_cell,
                                 ), className='my-3', 
                                 width=6),
          dbc.Col(dcc.Graph(id='player_graph'), width=6, className='my-3'),
     ], justify='left'),
     dbc.Row(
          id='gauges',
     )
     ], fluid=True)

@app.callback(
    [Output('player_tbl', 'data'),
     Output('player_tbl', 'columns'),
     Output('datatable_label', 'children'),
     Output('dataframe_feats', 'options'),
     Output('dataframe_feats', 'value'),
     Output('gauges', 'children')],
    [Input('skill_sets', 'value'),
     Input('position', 'value'),
     Input('player_graph', 'selectedData'),
     Input('player_tbl', 'columns')])
def update_datatable(skill_sets_dropdown, position_dropdown, selected_data, columns):
    if skill_sets_dropdown == 'Basic Player Data':
        df = basic_player_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        label_ = [f"{position_dropdown} Basic Player Data"]

        df['height_inches'] = df['height'].apply(feet_to_float)

    elif skill_sets_dropdown == 'Offense':
        df = offense_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        label_ = [f"{position_dropdown} Offensive Player Data"]
        # Formatting for % in data table and creating quantiles
        for col in df.columns:
          if "Pct" in col:
               df[col] = df[col]/100

    elif skill_sets_dropdown == 'Special Teams':
        df = special_team_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        label_ = [f"{position_dropdown} Special Teams Data"]
     
    elif skill_sets_dropdown == 'Endurance':
       df = endurance_data.copy()
       if position_dropdown != 'All Positions':
          df = df[df['name'] == position_dropdown].copy()
       else:
          df
       label_ = [f"{position_dropdown} Endurance Data"]

    else:
        df = enforcer_data.copy()
        if position_dropdown != 'All Positions':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        label_ = [f"{position_dropdown} Enforcer Data"]
    
    money = dash_table.FormatTemplate.money(2)

    if skill_sets_dropdown == 'Basic Player Data':
          
          columns = [
               dict(id='overall_rank',
                    name='Overall Rank'),
               dict(id='salary_rank',
                    name='Salary Rank',
                    type='numeric'),
               dict(id='fullName', 
                    name='Player Name'),
               dict(id='salary_2021-22',
                    name='Salary',
                    type='numeric',
                    format=money),
               dict(id='currentAge',
                    name='Age'),
               dict(id='height_inches',
                    name='Height (Inches)',
                    type='any'),
               dict(id='weight',
                    name='Weight'),
               dict(id='name', 
                    name='Position'),
               dict(id='shootsCatches',
                    name='Shoots'),
               dict(id='birthCountry',
                    name='Nationality'),
               dict(id='offense_overall_rank',
                    name='Offensive Overall Rank'),
               dict(id='special_teams_overall_rank',
                    name='Special Teams Overall Rank'),
               dict(id='enforcer_overall_rank',
                    name='Enforcer Overall Rank'),
               dict(id='endurance_overall_rank',
                    name='Endurance Overall Rank')
               ]

    elif skill_sets_dropdown == 'Offense':
          columns = [
               dict(id='salary_rank',
                    name='Salary Rank',
                    type='numeric'),
               dict(id='offense_overall_rank',
                    name='Offensive Player Rank',
                    type='numeric'),
               dict(id='fullName', name='Player Name'),
               dict(id='salary_2021-22',
                    name='Salary',
                    type='numeric',
                    format=money),
               dict(id='name',
                    name='Position'),
               dict(id='assists22',
                    name='Total Assists',
                    type='numeric'),
               dict(id='goals22',
                    name='Total Goals',
                    type='numeric'),
               dict(id='shots22',
                    name='Total Shots'),  
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

    elif skill_sets_dropdown == 'Special Teams':
          columns = [
               dict(id='salary_rank',
                    name='Salary Rank',
                    type='numeric'),
               dict(id='special_teams_overall_rank',
                    name='Special Teams Player Rank',
                    type='numeric'),
               dict(id='fullName',
                    name='Player Name'),
               dict(id='salary_2021-22',
                    name='Salary',
                    type='numeric',
                    format=money),\
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

    elif skill_sets_dropdown == 'Endurance':
          columns = [
               dict(id='salary_rank', 
                    name='Salary Rank'),
               dict(id='endurance_overall_rank', 
                    name='Endurance Player Rank'),
               dict(id='fullName', 
                    name='Player Name'),
               dict(id='salary_2021-22',
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

    else:
     columns = [
          dict(id='salary_rank',
               name='Salary Rank',
               type='numeric'),
          dict(id='enforcer_overall_rank',
               name='Enforcer Overall Rank',
               type='numeric'),
          dict(id='fullName', name='Player Name'),
          dict(id='salary_2021-22',
               name='Salary',
               type='numeric',
               format=money),
          dict(id='name',
               name='Position'),
          dict(id='hits22', name='Total Hits',type='numeric'),
          dict(id='penaltyMinutes22', name='Total Penalty Minutes', type='numeric')
]
    removed_cols = ['rank', 'salary']
    feats_dropdown = sorted([
                    col['name'] for col in columns \
                         if col['id'] in df.select_dtypes(['float64', 'int64']).columns \
                              if not any(unwanted_cols in col['id'] for unwanted_cols in removed_cols)
    ]) 

    df.sort_values('salary_rank', inplace=True)

    if selected_data is None:
     selected_player = df.iloc[0]['fullName']
    else:
     selected_player = selected_data['points'][0]['text']
    
    selected_player_stats = df[df['fullName'] == selected_player]
    dataframe_columns_ = []
    
    for col in df.columns:
     if df[col].dtype != 'object':
          if skill_sets_dropdown != 'Basic Player Data':
               if 'salary_rank' in col or 'salary' in col:
                    continue
               else:
                    dataframe_columns_.append(col)
          else:
               dataframe_columns_.append(col)

    changed_player = 'None'
    change = False
    
    if str(selected_player_stats['fullName'][0]) == str(changed_player):
          change = False
          raise PreventUpdate
    else:
          change = True

    gauges = []

    if change:
     for col in dataframe_columns_:
          qcut_bins = {}
          _, qcut_bins[f'{col}_bins'] = pd.qcut(df[col], 3, retbins=True)
          
          if 'rank' in col or 'Age' in col:
               gauges.append(dbc.Col(daq.Gauge(value=selected_player_stats[col][0],
                                             max=df[col].max(), 
                                             min=df[col].min(),
                                             size=150,
                                             label=[col_['name'] for col_ in columns if col_['id'] == col][0],
                                             color={'gradient':True,'ranges':{'green':[qcut_bins[f'{col}_bins'][0], qcut_bins[f'{col}_bins'][1]], 
                                                                                'yellow':[qcut_bins[f'{col}_bins'][1], qcut_bins[f'{col}_bins'][2]],
                                                                                'red':[qcut_bins[f'{col}_bins'][2], qcut_bins[f'{col}_bins'][3]]}})))

          else:
               gauges.append(dbc.Col(daq.Gauge(value=selected_player_stats[col][0],
                                             max=df[col].max(), 
                                             min=df[col].min(),
                                             size=150,
                                             label=[col_['name'] for col_ in columns if col_['id'] == col][0],
                                             color={'gradient':True,'ranges':{'red':[qcut_bins[f'{col}_bins'][0], qcut_bins[f'{col}_bins'][1]], 
                                                                                'yellow':[qcut_bins[f'{col}_bins'][1], qcut_bins[f'{col}_bins'][2]],
                                                                                'green':[qcut_bins[f'{col}_bins'][2], qcut_bins[f'{col}_bins'][3]]}})))
     changed_player = str(selected_player_stats['fullName'][0])
     change = False

    return df.to_dict('records'), \
           columns, \
           label_, \
           feats_dropdown, \
           feats_dropdown[0], \
           gauges

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

    if skill_sets_dropdown == 'Basic Player Data':
     # if columns != 'height'

     custom_data = np.stack((data_['overall_rank'], data_['salary_rank'], data_label_),axis=-1)

     hover_template = "<b>Player Name: </b> %{text} <br><br>"
     hover_template += "<b>%{customdata[2]}: </b> %{x} <br>"
     hover_template += "<b>Salary: </b> $%{y} <br>"
     hover_template += "<b>Salary Rank: </b> %{customdata[1]} <br>"
     hover_template += "<b>Player Rank: </b> %{customdata[0]}"

    elif skill_sets_dropdown == 'Offense':
     custom_data = np.stack((data_['offense_overall_rank'], data_['salary_rank'], data_label_),axis=-1)

     hover_template = "<b>Player Name: </b> %{text} <br><br>"
     hover_template += "<b>%{customdata[2]}: </b> %{x} <br>"
     hover_template += "<b>Salary: </b> $%{y} <br>"
     hover_template += "<b>Salary Rank: </b> %{customdata[1]} <br>"
     hover_template += "<b>Offensive Player Rank: </b> %{customdata[0]}"

    elif skill_sets_dropdown == 'Special Teams':
     custom_data = np.stack((data_['special_teams_overall_rank'], data_['salary_rank'], data_label_),axis=-1)

     hover_template = "<b>Player Name: </b> %{text} <br><br>"
     hover_template += "<b>%{customdata[2]}: </b> %{x} <br>"
     hover_template += "<b>Salary: </b> $%{y} <br>"
     hover_template += "<b>Salary Rank: </b> %{customdata[1]} <br>"
     hover_template += "<b>Special Teams Player Rank: </b> %{customdata[0]}"
    
    elif skill_sets_dropdown == 'Endurance':
     custom_data = np.stack((data_['endurance_overall_rank'], data_['salary_rank'], data_label_),axis=-1)

     hover_template = "<b>Player Name: </b> %{text} <br><br>"
     hover_template += "<b>%{customdata[2]}: </b> %{x} <br>"
     hover_template += "<b>Salary: </b> $%{y} <br>"
     hover_template += "<b>Salary Rank: </b> %{customdata[1]} <br>"
     hover_template += "<b>Endurance Player Rank: </b> %{customdata[0]}"

    else:
     custom_data = np.stack((data_['enforcer_overall_rank'], data_['salary_rank'], data_label_),axis=-1)

     hover_template = "<b>Player Name: </b> %{text} <br><br>"
     hover_template += "<b>%{customdata[2]}: </b> %{x} <br>"
     hover_template += "<b>Salary: </b> $%{y} <br>"
     hover_template += "<b>Salary Rank: </b> %{customdata[1]} <br>"
     hover_template += "<b>Enforcer Player Rank: </b> %{customdata[0]}"
   
    fig = go.Figure(go.Scatter(
                        x=data_[str(col_name)],
                        y=data_['salary_2021-22'],
                        mode='markers',
                        text=data_['fullName'],
                        customdata=custom_data,
                        hovertemplate=hover_template,
                        showlegend=False,
                        name='playerName',

                        ))

    fig.update_layout(title_text= f"<em>Group:</em>{skill_sets_dropdown} <em>Position:</em>{position_dropdown} <em>Data:</em>{feature}",
                      title_y=0.96,
                      title_x=0.5,
                      xaxis_title=f"<b>{x_axis_label}</b>",
                      yaxis_title="<b>Player Salaries 2021-22</b>",
                      autosize=True,
                      clickmode='event+select',
                      margin=dict(
                         l=15,
                         r=15,
                         b=15,
                         t=50,
                         pad=4)
                      )

    return [fig]