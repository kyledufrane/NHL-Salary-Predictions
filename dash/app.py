import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True)

app.config.external_stylesheets = [dbc.themes.CERULEAN]

server = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Collapse(
                    dbc.Nav([
                        dbc.NavItem(
                            dbc.NavLink(
                                'Player Search',
                                href='/'
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "What's My Worth?",
                                href='/player-worth',
                            ),
                            className='me-auto'
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                'About',
                                href='/about'
                            )
                        )
                    ],
                        className='w-100'
                    ),
                    is_open=False,
                    navbar=True
                )
            ],
                className='flex-grow-1'
            )

        ],
            fluid=True
        ),
        dark=True,
        color='primary'
    ),
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)

