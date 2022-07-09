from dash import html, dcc
import dash_bootstrap_components as dbc


layout = dbc.Container(
    [
        dbc.Row(
            html.H3(
                'About',
                style={
                    'textAlign': 'center'
                }
            ),
            className='my-5'
        ),
        dbc.Row(
            html.H3(
                'This project was inspired while I was attending Flatirons Data Science Bootcamp. While working '
                'through the course, '
                'I\'d have code up on one monitor with the Stanley Cup Finals on the other. At the time, '
                'I had two things on my mind '
                'the NHL and boot camp. When it came down to the Capstone Project, I decided to build an '
                'application to predict NHL players '
                'salaries allowing players or the NHLPA to find proper contract amounts.'
            ),
            style={
                'textAlign': 'center',
                'margin-bottom': '15px'
            }
        ),
        dbc.Row(
            html.H3(
                'I used two methods to collect the data:'
            ),
            style={
                'textAlign': 'center'
            },
        ),
        dbc.Row(
            html.H3(
                '- NHL.com’s API - player statistics'
            ),
            style={
                'textAlign': 'center'
            }
        ),
        dbc.Row(
            html.H3(
                '- Web Scraping - contract amounts.'
            ),
            style={
                'textAlign': 'center',
                'margin-bottom': '15px'
            }
        ),
        dbc.Row(
            html.H3(
                'After the data cleaning process, the project utilizes SciKit-Learn for modeling and Tune '
                'SKLearn, from the Ray library, '
                'for hyperparameter optimization. The project performed well with a mean absolute error of ~$1,'
                '115,000. '
            ),
            style={
                'textAlign': 'center',
                'margin-bottom': '15px'
            }
        ),
        dbc.Row(
            html.H3(
                'The application was built using Plotly Dash and hosted on Heroku.'
            ),
            style={
                'textAlign': 'center',
                'margin-bottom': '25px',
                'font-size': '25px'
            }
        ),
        dbc.Row(
            html.H3(
                'For more information on the project and libraries used visit the below links:'
            ),
            style={
                'textAlign': 'center',
                'margin-bottom': 'center',
                'font-size': '25px',
                'margin-bottom': '25px'
            }
        ),
        dbc.Row(
            dcc.Link(
                'Project Repo - Github',
                href='https://github.com/kyledufrane/NHL-Salary-Predictions',
                style={
                    'textAlign': 'center',
                    'margin-bottom': '15px',
                    'font-size': '25px'
                }
            )
        ),
        dbc.Row(
            dcc.Link(
                'SciKit-Learn',
                href='https://scikit-learn.org/stable/',
                style={
                    'textAlign': 'center',
                    'margin-bottom': '15px',
                    'font-size': '25px'
                }
            )
        ),
        dbc.Row(
            dcc.Link(
                'Tune SKLearn [Ray]',
                href='https://docs.ray.io/en/latest/tune/api_docs/sklearn.html',
                style={
                    'textAlign': 'center',
                    'margin-bottom': '15px',
                    'font-size': '25px'
                }
            )
        ),
        dbc.Row(
            dcc.Link(
                'Plotly Dash',
                href='https://plotly.com/dash/',
                style={
                    'textAlign': 'center',
                    'margin-bottom': '15px',
                    'font-size': '25px'
                }
            )
        )
    ]
)
