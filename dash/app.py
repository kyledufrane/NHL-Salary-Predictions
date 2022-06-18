import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
                          meta_tags=[{'name': 'viewport',
                                      'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

app.config.suppress_callback_exceptions=True

# CERULEAN, 
# COSMO, 
# CYBORG, 
# DARKLY, 
# FLATLY, 
# JOURNAL, 
# LITERA, 
# LUMEN, 
# LUX, 
# MATERIA, 
# MINTY, 
# MORPH, 
# PULSE, 
# QUARTZ, 
# SANDSTONE, 
# SIMPLEX, 
# SKETCHY, 
# SLATE, 
# SOLAR, 
# SPACELAB, 
# SUPERHERO, 
# UNITED, 
# VAPOR, 
# YETI, 
# ZEPHYR