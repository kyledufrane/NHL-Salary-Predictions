from dash import html
import plotly.figure_factory as ff
import pandas as pd

# --------------------------- Column Filters After Formatting------------------------------------------

basic_player = (
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
)
offense = (
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
)
special_teams = (
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
)
enforcer = (
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
)
endurance = (
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
)

def filter_data(skill_sets_dropdown, position_dropdown):
    df = pd.read_csv('https://raw.githubusercontent.com/kyledufrane/NHL-Salary-Predictions/main/data/dash_cleaned_player_data.csv')
    # Filter dataframes based on dropdowns
    filters = ()
    skill_sets_dropdown_ = [skill_sets_dropdown]
    if len(skill_sets_dropdown_[0]) > 1 and len(skill_sets_dropdown_[0]) <= 5:
        for filter_ in skill_sets_dropdown_[0]:
            if filter_ == 'Basic Player Data':
                filters += basic_player
            elif filter_ == 'Offense':
                filters += offense
            elif filter_ == 'Special Teams':
                filters += special_teams
            elif filter_ == 'Endurance':
                filters += endurance
            else:
                filters += enforcer       
    else:
        if skill_sets_dropdown == 'Basic Player Data':
            filters = basic_player
        elif skill_sets_dropdown == 'Offense':
            filters = offense
        elif skill_sets_dropdown == 'Special Teams':
            filters = special_teams
        elif skill_sets_dropdown == 'Endurance':
            filters = endurance
        else:
            filters = enforcer
    df_ = filter_data_position(df[list(set(filters))], position_dropdown)
    return df_

def filter_data_position(df, position_dropdown):
    if position_dropdown != 'All Positions':
        df_ = df[df['Position'].str.contains('|'.join(position_dropdown))]
        return df_
    else:
        return df

def select_columns(df_, skill_sets_dropdown):
    if 'Basic Player Data' in skill_sets_dropdown:
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
    return sorted(list(set(wanted_columns)))

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
    player_name = 'Please Select A Player'
    stats_values = [
            html.H3(children='No Data', style={'textAlign': 'center'})
            for val in wanted_columns
        ]
    salary_rank = 0
    overall_rank = 0
    offensive_rank = 0
    special_teams_rank = 0
    enforcer_rank = 0
    endurance_rank = 0

    return player_name, \
        stats_values, \
        salary_rank, \
        overall_rank, \
        offensive_rank, \
        special_teams_rank, \
        enforcer_rank, \
        endurance_rank
