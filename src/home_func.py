from distutils.command.build import build
from dash import html, dash_table, Input, Output, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import pandas as pd


# --------------------------- Column Filters After Formatting------------------------------------------
basic_player = [
    'id',
    'Overall Rank',
    'Salary Rank',
    'Player Name',
    'Salary',
    'Age',
    'Height (Inches)',
    'Height',
    'Weight',
    'Position',
    'Shoots',
    'Nationality',
    'Offensive Overall Rank',
    'Special Teams Overall Rank',
    'Enforcer Overall Rank',
    'Endurance Overall Rank'
]
offense = [
    'id',
    'Salary Rank',
    'Player Name',
    'Salary',
    'Position',
    'Overall Rank',
    'Offensive Overall Rank',
    'Special Teams Overall Rank',
    'Enforcer Overall Rank',
    'Endurance Overall Rank',
    'Total Assists',
    'Total Goals',
    'Total Shots',
    'Face Off Percentage',
    'Shot Percentage',
    'Game Winning Goals',
    'Over Time Goals',
    'Points',
    'Plus Minus'
]
special_teams = [
    'id',
    'Salary Rank',
    'Player Name',
    'Salary',
    'Position',
    'Overall Rank',
    'Offensive Overall Rank',
    'Special Teams Overall Rank',
    'Enforcer Overall Rank',
    'Endurance Overall Rank',
    'Power Play Goals',
    'Power Play Points',
    'Power Play Time On Ice',
    'Short Handed Goals',
    'Short Handed Points',
    'Short Handed Time On Ice'
]
enforcer = [
    'id',
    'Salary Rank',
    'Player Name',
    'Salary',
    'Position',
    'Overall Rank',
    'Offensive Overall Rank',
    'Special Teams Overall Rank',
    'Enforcer Overall Rank',
    'Endurance Overall Rank',
    'Total Hits',
    'Total Penalty Minutes'
]
endurance = [
    'id',
    'Salary Rank',
    'Player Name',
    'Salary',
    'Position',    
    'Overall Rank',
    'Offensive Overall Rank',
    'Special Teams Overall Rank',
    'Enforcer Overall Rank',
    'Endurance Overall Rank',
    'Time On Ice',
    'Total Games',
    'Total Shifts',
    'Blocked Shots',
    'Time On Ice Per Game',
    'Even Time On Ice Per Game',
    'Short Handed Time On Ice Per Game',
    'Power Play Time On Ice Per Game'
]



def filter_data(skill_sets_dropdown, position_dropdown):
    df = pd.read_csv('https://raw.githubusercontent.com/kyledufrane/NHL-Salary-Predictions/main/data/dash_cleaned_player_data.csv')
    # Filter dataframes based on dropdowns
    if skill_sets_dropdown == 'Basic Player Data':
        df_ = filter_data_position(df, position_dropdown, basic_player)
    elif skill_sets_dropdown == 'Offense':
        df_ = filter_data_position(df, position_dropdown, offense)
    elif skill_sets_dropdown == 'Special Teams':
        df_ = filter_data_position(df, position_dropdown, special_teams)
    elif skill_sets_dropdown == 'Endurance':
        df_ = filter_data_position(df, position_dropdown, endurance)
    else:
        df_ = filter_data_position(df, position_dropdown, enforcer)

    return df_

def filter_data_position(df, position_dropdown, col_filter):
    df_ = df.loc[:, col_filter]
    if position_dropdown != 'All Positions':
        df_ = df_[df_['Position'] == position_dropdown].copy()
    else:
        df_
    return df_

def select_columns(df_, skill_sets_dropdown):
    if skill_sets_dropdown == 'Basic Player Data':
        wanted_columns = [
            col_name for col_name in df_.columns
            if df_[col_name].dtype != 'object'
            and 'Inches' not in col_name
            and 'Rank' not in col_name
            and 'Salary' not in col_name
        ]
        wanted_columns.append('Height')
        
    else:    
        wanted_columns = [
        col_name for col_name in df_.columns
        if df_[col_name].dtype != 'object'
        and 'Rank' not in col_name
        and 'Salary' not in col_name
    ]
    return sorted(wanted_columns)

def build_plot(dataframe_features_dropdown_value, df_, data, hover_template, customdata):
    fig = ff.create_distplot([df_[data]], [dataframe_features_dropdown_value], show_hist=False)
    fig.update_traces(hovertemplate=hover_template,
                    customdata=customdata)
    fig.update_layout(showlegend=False, 
                        margin=dict(l=0, r=0, t=0, b=0),
                        clickmode='event+select',
                        xaxis_tickformat=',d')
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    return fig

def return_default_values(wanted_columns):
    player_name = 'Please Select A Player To View Their Stats'
    stats_values = [
        html.H3(children=val, style={'textAlign': 'center'})
        for val in list('No Data' for i in range(len(wanted_columns)))
    ]
    salary_rank = 0
    overall_rank = 0
    offensive_rank = 0
    special_teams_rank = 0
    enforcer_rank = 0
    endurance_rank = 0

    return player_name,  \
            stats_values,  \
            salary_rank,  \
            overall_rank,  \
            offensive_rank, \
            special_teams_rank, \
            enforcer_rank, \
            endurance_rank 