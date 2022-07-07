from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
# import all pages in the app
from apps import home, player_worth, about

app.layout = html.Div([
    dcc.Location(
        id='url',
        refresh=False
    ),
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
                                    href='/player_worth',
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
    html.Div(
        id='page-content'
    )
])


@ app.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/player_worth':
        return player_worth.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/home' or pathname == '/':
        return home.layout
    else:
        return html.Div(
            dbc.Container([
                html.H1('404 Not Found', className='display-3'),
                html.P('Webpage Not Found', className='lead')
            ]))


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True, port=8051)

#%%
