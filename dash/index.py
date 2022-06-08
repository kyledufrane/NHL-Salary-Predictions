from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
# import all pages in the app
from apps import home, player_comparison, player_worth

# button_group = dbc.ButtonGroup([
#     dbc.Button('Player Comparison', outline=True, href='/player_comparison'),
#     dbc.Button("What's my worth?", outline=True, href='/player_worth')
# ])

nav = dbc.Nav([
    dbc.NavItem(dbc.NavLink('Player Comparison', active=True, href='/player_comparison')),
    dbc.NavItem(dbc.NavLink("What's my worth?", active=True, href='/player_worth'))
])

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/nhl.png", height="50px")),
                        dbc.Col(dbc.NavbarBrand("NHLPA SALARY NEGOTIATOR", class_name="ms-2")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            nav
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/player_comparison':
        return player_comparison.layout
    elif pathname == '/player_worth':
        return player_worth.layout
    elif pathname =='/home' or pathname=='/':
        return home.layout
    else:
        return html.Div(
        dbc.Container([
            html.H1('404 Not Found', className='display-3'),
            html.P('Webpage Not Found', className='lead')
        ]))

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)