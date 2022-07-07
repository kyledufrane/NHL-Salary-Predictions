from dash import html
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
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
    'PP Goals',
    'PP Points',
    'PP TOI',
    'Short Handed Goals',
    'Short Handed Points',
    'Short Handed TOI'
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
    'Total TOI',
    'Total Games',
    'Total Shifts',
    'Blocked Shots',
    'TOI PG',
    'Even TOI PG',
    'Short Handed TOI PG',
    'PP TOI PG'
)


def filter_data(skill_sets_dropdown, position_dropdown):
    df = pd.read_csv(
        'https://raw.githubusercontent.com/kyledufrane/NHL-Salary-Predictions/main/data/dash_cleaned_player_data.csv'
    )
    # Filter dataframes based on dropdowns
    filters = ()
    skill_sets_dropdown_ = [skill_sets_dropdown]
    if 1 < len(skill_sets_dropdown_[0]) <= 5:
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
        if skill_sets_dropdown[0] == 'Basic Player Data':
            filters = basic_player
        elif skill_sets_dropdown[0] == 'Offense':
            filters = offense
        elif skill_sets_dropdown[0] == 'Special Teams':
            filters = special_teams
        elif skill_sets_dropdown[0] == 'Endurance':
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
        wanted_columns = []
        for col in df_.columns:
            if df_[col].dtype != 'object' \
                    and 'Inches' not in col \
                    and 'Rank' not in col \
                    and 'Salary' not in col:
                wanted_columns.append(col)
        wanted_columns.append('Height')

    else:
        wanted_columns = []
        for col_name in df_.columns:
            if df_[col_name].dtype != 'object' \
                    and 'Rank' not in col_name \
                    and 'Salary' not in col_name:
                wanted_columns.append(col_name)

    return sorted(list(set(wanted_columns)))


def build_stats_columns(df_, wanted_columns):
    if len(df_) == 0:
        return return_default_values(wanted_columns)

    else:
        basic_player_ = [col for col in wanted_columns if col in basic_player]
        offense_ = [col for col in wanted_columns if col in offense]
        special_teams_ = [col for col in wanted_columns if col in special_teams]
        endurance_ = [col for col in wanted_columns if col in endurance]
        enforcer_ = [col for col in wanted_columns if col in enforcer]

        stats_row_ = []

        def format_columns(df_, filter_):

            style_ = {
                'textAlign': 'center'
            }

            if filter_ == basic_player_:
                text = 'Basic'
            elif filter_ == offense_:
                text = 'Offense'
            elif filter_ == special_teams_:
                text = 'Special Teams'
            elif filter_ == endurance_:
                text = 'Endurance'
            else:
                text = 'Enforcer'

            if len(filter_) >= 1:
                stats_row_ = dbc.Row([
                    dbc.Col(
                        html.H4(
                            text,
                            style=style_,
                            # className='border rounded-2 border-primary'
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dbc.Row(
                            [
                                html.H4(children=col, style={'textAlign': 'center'})
                                for col in filter_
                            ])
                    ),
                    dbc.Col(
                        dbc.Row([
                            html.H4(children=df_[val], style={'textAlign': 'center'})
                            for val in filter_
                        ])
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
                ],
                    justify='center',
                    align='center'
                )
                return stats_row_
            else:
                return None

        stats_row_.append(format_columns(df_, basic_player_))
        stats_row_.append(format_columns(df_, offense_))
        stats_row_.append(format_columns(df_, special_teams_))
        stats_row_.append(format_columns(df_, endurance_))
        stats_row_.append(format_columns(df_, enforcer_))

        return stats_row_


def build_plot(dataframe_features_dropdown_value, df_, data, hover_template, customdata):
    fig = ff.create_distplot([df_[data]], [dataframe_features_dropdown_value], show_hist=False)
    fig.update_traces(
        hovertemplate=hover_template,
        customdata=customdata
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        clickmode='event+select',
        xaxis_tickformat=',d'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    fig.update_yaxes(
        visible=False
    )
    fig.update_xaxes(
        visible=False
    )
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

    return player_name, stats_values, salary_rank, overall_rank, offensive_rank, special_teams_rank, enforcer_rank, \
        endurance_rank


def add_legend():
    return dbc.Row(
        dbc.Col([
            dbc.Row(
                html.H3(
                    'Legend',
                    style={
                        'textAlign': 'center',
                        'text-decoration': 'underline'
                    }
                ),
            ),
            dbc.Row(
                html.H4(
                    'PP: Power Play'
                )
            ),
            dbc.Row(
                html.H4(
                    'TOI: Time On Ice'
                )
            ),
            dbc.Row(
                html.H4(
                    'PG: Per Game'
                )
            )
        ],
            style={
                'textAlign': 'center',
                'border': '2px black solid'
            },
            className='my-5'
        )
    )
