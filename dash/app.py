import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__) #,
                          # meta_tags=[{'name': 'viewport',
                          #             'content': 'width=device-width, initial-scale=1.0'}])
app.config.external_stylesheets = [dbc.themes.SLATE]

server = app.server

app.config.suppress_callback_exceptions = True

# CERULEAN, 
# COSMO, 
# CYBORG, 
# DARKLY, 
# FLATLY, 
# JOURNAL, 
# LITERA, 
# LUMEN, 
# LUX, #
# MATERIA, 
# MINTY, 

# PULSE, 
# QUARTZ, 
# SANDSTONE, 
# SIMPLEX, 
# SKETCHY, 

# SOLAR, 
# SPACELAB, 
# SUPERHERO, 
# UNITED, 
# VAPOR, 
# YETI, 
# ZEPHYR




# MORPH,
# SLATE,