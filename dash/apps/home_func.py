from distutils.command.build import build
from dash import html, dash_table, Input, Output, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import pandas as pd

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