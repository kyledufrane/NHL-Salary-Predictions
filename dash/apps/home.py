from dash import html, dash_table, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# --------------------------- Dataframes ------------------------------------------------------

columns = ['birthDate',
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
           'birthCity']

df = pd.read_csv('~/Desktop/NHL-Salary-Predictions/data/cleaned_player_df_dash.csv').drop(columns, axis=1)
df['shootsCatches'] = df['shootsCatches'].replace('L', 'Left').replace('R', 'Right')

# --------------------------- Player Salaries -------------------------------------------------

df = df[df['Salary_2020-21'] != 0.0]
df_datatable_1 = df[['fullName',
                     'Salary_2020-21',
                     'name',
                     'currentAge',
                     'height',
                     'weight',
                     'shootsCatches',
                     'birthCountry']] \
                    .sort_values('Salary_2020-21', ascending=False)
df_datatable_1['shootsCatches'] = df_datatable_1['shootsCatches'].replace('L', 'Left').replace('R', 'Right')
df_datatable_1['Rank'] = range(1, len(df_datatable_1) + 1)
df_datatable_1 = df_datatable_1[['Rank',
                                 'fullName',
                                 'Salary_2020-21',
                                 'name',
                                 'currentAge',
                                 'height',
                                 'weight',
                                 'shootsCatches',
                                 'birthCountry']]
df_datatable_1['id'] = df['fullName']
df_datatable_1.set_index('id', inplace=True, drop=False)

# --------------------------- Offensive Stat's -------------------------------------------------

offense = df[['fullName',
              'timeOnIce20',
              'assists20',
              'goals20',
              'pim20',
              'shots20',
              'games20',
              'hits20']]
offense['timeOnIce20'] = offense['timeOnIce20'].str.replace(':', '.').astype(float)
offense.fillna(0.0, inplace=True)

# --------------  Player Salaries DF - formatting salaries -----------------------------------

money = dash_table.FormatTemplate.money(2)

salary_columns = [
    dict(id='Rank', name='Rank', type='numeric'),
    dict(id='fullName', name='Player Name'),
    dict(id='Salary_2020-21', name='Salary 2020-21', type='numeric', format=money),
    dict(id='name', name='Position'),
    dict(id='currentAge', name='Age'),
    dict(id='height', name='Height', type='any'),
    dict(id='weight', name='Weight'),
    dict(id='shootsCatches', name='Shoots'),
    dict(id='birthCountry', name='Nationality')
]

active_cell = {'row': 0, 'column': 1, 'column_id': 'Player Name', 'row_id': 0}

offense_columns = [
    dict(id='fullName', name='Player Name'),
    dict(id='timeOnIce20', name='Total Time On Ice', type='numeric'),
    dict(id='assists20', name='Total Assists', type='numeric'),
    dict(id='goals20', name='Total Goals', type='numeric'),
    dict(id='pim20', name='Total Penalty Minutes', type='numeric'),
    dict(id='shots20', name='Total Shots', type='numeric'),
    dict(id='games20', name='Total Games', type='numeric'),
    dict(id='hits20', name='Total Hits', type='numeric')
]

# --------------------------- Filtering Operators --------------------------------------------

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

# --------------------------- Visualizations -------------------------------------------------

def discrete_background_color_bins(df, n_bins=5, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max()
    df_min = df_numeric_columns.min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
        ]
    ranges = pd.DataFrame(ranges)
    styles = []
    legend = []
    for column in df_numeric_columns:

        for i in range(1, len(bounds)):
            min_bound = ranges[column][i - 1]
            max_bound = ranges[column][i]
            backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
            color = 'white' if i > len(bounds) / 2. else 'black'

            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        # legend.append(
        #     html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
        #         html.Div(
        #             style={
        #                 'backgroundColor': backgroundColor,
        #                 'borderLeft': '1px rgb(50, 50, 50) solid',
        #                 'height': '10px'
        #             }
        #         ),
        #         html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
        #     ])
        # )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

(styles, legend) = discrete_background_color_bins(offense)

# --------------------------- Page Layout ----------------------------------------------------

layout = html.Div(
    className="row",
    children=[
        html.Div([
            html.H5('Player Salaries', style={'text-align': 'center',
                                              'text-decoration': 'underline'}),
            dash_table.DataTable(columns = salary_columns,
                                 data=df_datatable_1.to_dict('records'),
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
                                 active_cell=active_cell,
                                 id='player_tbl')],
            style={'height': 450, 'width':'50%',
                   'overflowX': 'scroll',
                   'display': 'inline-block',
                   'vertical-align': 'top',
                   'margin-left': '3vw',
                   'margin-top': '3vw'}
            ),
        html.H5('Player Salary Comparison', style={'text-align': 'center',
                                                  'text-decoration': 'underline',
                                                  'margin-top': '3vw',
                                                  'height': '1vh'}),
        html.Div(id='output_graph',
                style={'display': 'inline-block', 
                       'vertical-align': 'top', 
                       'margin-left': '3vw', 
                       'margin-top': '3vw',
                       'width': '95%'}),
        html.Div([
                html.Div(legend, style={'float': 'right'}),
                dash_table.DataTable(
                    id='offense_tbl',
                    data=offense.to_dict('records'),
                    sort_action='native',
                    columns=offense_columns,
                    style_data_conditional=styles,
                    style_data={'color': 'black',
                                'backgroundColor': 'white',
                                'border': '1px solid black'},
                    style_header={'backgroundColor': 'white', 
                                  'color': 'black',
                                  'fontWeight': 'bold',
                                  'border': '1px solid black'},
    ),
])
    ]
)

# ---------------- Player Salaries Filtering Definitions -------------------------------------


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-filtering-be', "data"),
    Input('table-filtering-be', "filter_query"))
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_dict('records')

# ---------------- Interactive Graph -------------------------------------

@app.callback(
    Output('output_graph', 'children'),
    Input('player_tbl', 'derived_virtual_row_ids'),
    Input('player_tbl', 'selected_row_ids'),
    Input('player_tbl', 'active_cell'))
def update_graphs(row_ids, selected_row_ids, active_cell):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    selected_id_set = set(selected_row_ids or [])
    
    if row_ids is None:
        dff = df_datatable_1
        # pandas Series works enough like a list for this to be OK
        row_ids = df_datatable_1['id']
    else:
        dff = df_datatable_1.loc[row_ids]

    active_row_id = active_cell['row_id'] if active_cell else None

    colors = ['#FF69B4' if id == active_row_id
              else '#7FDBFF' if id in selected_id_set
              else '#0074D9'
              for id in row_ids]

    return dcc.Graph(
            id='Player_Salary_Comparison',
            figure={
                'data': [
                    {
                        'x': dff['id'],
                        'y': dff['Salary_2020-21'],
                        'type': 'bar',
                        'marker': {'color': colors},
                    }
                ],
                'layout': {
                    'xaxis': {
                        'automargin': True,
                        'title' : {'text': 'Player Name'}
                    },
                    'yaxis': {
                        'automargin': True,
                        'title': {'text': 'Salary 2020-21'}
                    },
                    'height': 250,
                    'margin': {'t': 10, 'l': 10, 'r': 10},
                },
            },
        )
