from dataclasses import dataclass
from dash import html, dash_table, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

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
                'birthCountry']
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
    dbc.Row([
        dbc.Col([
            html.H5(id='datatable_label',
                    style={'text-align':'center',
                          'text-decoration':'underline'}),
            dash_table.DataTable(id='player_tbl',
                                 filter_action='native',
                                 sort_action="native",
                                 style_cell={'textAlign': 'right'},
                                 style_as_list_view=True,
                                 style_data={'color': 'black',
                                             'backgroundColor': 'white',
                                             'border': '1px solid black'},
                                 style_header={'backgroundColor': 'white',
                                               'color': 'black',
                                               'fontWeight': 'bold',
                                               'border': '1px solid black'},
                                 active_cell=active_cell,)
                                #  filter_query='')
    ],style={'height': 450, 'width':'50%',
                   'overflowX': 'scroll',
                   'display': 'inline-block',
                   'vertical-align': 'top',
                   'margin-left': '3vw',
                   'margin-top': '0vw'}),
        dbc.Col([
            dcc.Dropdown(options=['Basic Player Data',
                                 'Offense',
                                #  'Defense',
                                 'Special Teams',
                                 'Enforcer'
            ], 
            value='Basic Player Data', 
            id='skill_sets')
        ], width=3,
           style={'margin-top': '5vw'}),
        dbc.Col([
            dcc.Dropdown(options=['All',
                                  'Center',
                                  'Right Wing',
                                  'Left Wing',
                                  'Defenseman'],
                        value='All',
                        id='position')
        ], width=3,
           style={'margin-top': '5vw'})
    ])
])

@app.callback(
    [Output('player_tbl', 'data'),
     Output('player_tbl', 'columns'),
     Output('datatable_label', 'children')],
    [Input('skill_sets', 'value'),
    Input('position', 'value'),]
    # Input('player_tbl', "filter_query")]
)
def update_datatable(skills_sets_dropdown, position_dropdown):
    if skills_sets_dropdown == 'Basic Player Data':
        df = basic_player_data.copy()
        if position_dropdown != 'All':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = basic_player_columns
        label_ = f"{position_dropdown} Basic Player Data"
    
    elif skills_sets_dropdown == 'Offense':
        df = offense_data.copy()
        if position_dropdown != 'All':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = offensive_columns
        label_ = f"{position_dropdown} Offensive Player Data"

    elif skills_sets_dropdown == 'Special Teams':
        df = special_team_data.copy()
        if position_dropdown != 'All':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = special_teams_columns    
        label_ = f"{position_dropdown} Special Teams Data"

    else:
        df = enforcer_data.copy()
        if position_dropdown != 'All':
            df = df[df['name'] == position_dropdown].copy()
        else:
            df
        columns = enforcer_columns
        label_ = f"{position_dropdown} Enforcer Data"

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
    df['overall_rank'] = df['sum_quantiles'].rank(method='first', ascending=False).astype('int64')

    return df.to_dict('records'), columns, label_
# ---------------- Player Salaries Filtering Definitions -------------------------------------

# @app.callback(
#     Output('player_tbl', "data"),
#     Input('player_tbl', "filter_query"))
# def update_table(filter):
#     filtering_expressions = filter.split(' && ')
#     dff = basic_player_data.copy()
#     for filter_part in filtering_expressions:
#         col_name, operator, filter_value = split_filter_part(filter_part)

#         if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
#             # these operators match pandas series operator method names
#             dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
#         elif operator == 'contains':
#             dff = dff.loc[dff[col_name].str.contains(filter_value)]
#         elif operator == 'datestartswith':
#             # this is a simplification of the front-end filtering logic,
#             # only works with complete fields in standard format
#             dff = dff.loc[dff[col_name].str.startswith(filter_value)]

#     return dff.to_dict('records')


# # ---------------- Interactive Graph -------------------------------------

# # @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )


# # --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display':# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'colo# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied # --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],# --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i # --------------------------- Page Content -------------------------------------------------

# # def discrete_background_color_bins(df, n_bins=5, columns='all'):
# #     import colorlover
# #     bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])in range(n_bins + 1)]
# #     if columns == 'all':
# #         if 'id' in df:
# #             df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
# #         else:
# #             df_numeric_columns = df.select_dtypes('number')
# #     else:
# #         df_numeric_columns = df[columns]
# #     df_max = df_numeric_columns.max()
# #     df_min = df_numeric_columns.min()
# #     ranges = [
# #         ((df_max - df_min) * i) + df_min
# #         for i in bounds
# #         ]
# #     ranges = pd.DataFrame(ranges)
# #     styles = []
# #     legend = []
# #     for column in df_numeric_columns:

# #         for i in range(1, len(bounds)):
# #             min_bound = ranges[column][i - 1]
# #             max_bound = ranges[column][i]
# #             backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
# #             color = 'white' if i > len(bounds) / 2. else 'black'

# #             styles.append({
# #                 'if': {
# #                     'filter_query': (
# #                         '{{{column}}} >= {min_bound}' +
# #                         (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
# #                     ).format(column=column, min_bound=min_bound, max_bound=max_bound),
# #                     'column_id': column
# #                 },
# #                 'backgroundColor': backgroundColor,
# #                 'color': color
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])or': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])l_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])r': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])
# #             })
# #         # legend.append(
# #         #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
# #         #         html.Div(
# #         #             style={
# #         #                 'backgroundColor': backgroundColor,
# #         #                 'borderLeft': '1px rgb(50, 50, 50) solid',
# #         #                 'height': '10px'
# #         #             }
# #         #         ),
# #         #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
# #         #     ])
# #         # )

# #     return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# # (styles, legend) = discrete_background_color_bins(offense)

# # graph = dbc.Card(
# #                 children=[
# #                     dbc.CardBody([
# #                         html.Div([
# #                             dcc.Graph(
# #                                     id="main-graph",
# #                                     figure={
# #                                         "layout":{
# #                                             "margin": {"t":30, "r":35, "b":40, "l":50},
# #                                             "xaxis": {
# #                                                 "dtick": 5,
# #                                                 "gridcolor": "#636363",
# #                                                 "showline": False
# #                                             },
# #                                             "yaxis":{"showgrid": False, "showline": False},
# #                                             "plot_bgcolor": "black",
# #                                             "paper_bgcolor": "black",
# #                                             "font": {"color": "gray"},
# #                                         },
# #                                     },
# #                                     config={'displayModeBar': False},
# #                             ),
# #                             html.Pre(id="update-on-click-data"),
# #                         ],
# #                         style={"width": "98%", "display": "inline-block"},
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='feature-dropdown',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                       @app.callback(
# #     Output('output_graph', 'children'),
# #     Input('player_tbl', 'derived_virtual_row_ids'),
# #     Input('player_tbl', 'selected_row_ids'),
# #     Input('player_tbl', 'active_cell'))
# # def update_graphs(row_ids, selected_row_ids, active_cell):
# #     # When the table is first rendered, `derived_virtual_data` and
# #     # `derived_virtual_selected_rows` will be `None`. This is due to an
# #     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
# #     # calls the dependent callbacks when the component is first rendered).
# #     # So, if `rows` is `None`, then the component was just rendered
# #     # and its value will be the same as the component's dataframe.
# #     # Instead of setting `None` in here, you could also set
# #     # `derived_virtual_data=df.to_rows('dict')` when you initialize
# #     # the component.
# #     selected_id_set = set(selected_row_ids or [])
    
# #     if row_ids is None:
# #         dff = basic_player_data.copy()
# #         # pandas Series works enough like a list for this to be OK
# #         row_ids = basic_player_data['id']
# #     else:
# #         dff = basic_player_data.loc[row_ids]

# #     active_row_id = active_cell['row_id'] if active_cell else None

# #     colors = ['#FF69B4' if id == active_row_id
# #               else '#7FDBFF' if id in selected_id_set
# #               else '#0074D9'
# #               for id in row_ids]

# #     return dcc.Graph(
# #             id='Player_Salary_Comparison',
# #             figure={
# #                 'data': [
# #                     {
# #                         'x': dff['id'],
# #                         'y': dff['Salary_2021-22'],
# #                         'type': 'bar',
# #                         'marker': {'color': colors},
# #                     }
# #                 ],
# #                 'layout': {
# #                     'xaxis': {
# #                         'automargin': True,
# #                         'title' : {'text': 'Player Name'}
# #                     },
# #                     'yaxis': {
# #                         'automargin': True,
# #                         'title': {'text': 'Salary 2020-21'}
# #                     },
# #                     'height': 250,
# #                     'margin': {'t': 10, 'l': 10, 'r': 10},
# #                 },
# #             },
# #         )
#   ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
# #                     html.Div([
# #                         dcc.Dropdown(
# #                             id='player-name',
# #                             options=[
# #                                 {"label": label, "value": label} for label in df.columns if label != 'fullName'
# #                             ],
# #                             value="",
# #                             multi=False,
# #                             searchable=True
# #                             )
# #                         ],
# #                     style={
# #                         "width": "33%",
# #                         "display": "inline-block",
# #                         "color": "black"
# #                         },
# #                     ),
            
# #             ])
# #         ])