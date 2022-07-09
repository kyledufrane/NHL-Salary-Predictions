import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

app.config.external_stylesheets = [dbc.themes.CERULEAN]

server = app.server

app.config.suppress_callback_exceptions = True

