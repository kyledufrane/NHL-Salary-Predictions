from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc

def add_header(header):
    return html.H4(
        header,
        style={
            'textAlign': 'center',
            'text-decoration': 'underline'
        },
        className='py-3'
    )


def add_slider_input(df, data):
    return dbc.Row([
        dbc.Col(
            dcc.Slider(
                id=f'{data}_slider',
                min=0,
                max=df[data].max() * 1.25,
                value=round(df[data].mean()),
                step=1,
                marks=None,
                className='my-2'
            ),
            style={
                'textAlign': 'left'
            }
        ),
        dbc.Col(
            dcc.Input(
                id=f"{data}_input",
                type='number',
                value=round(df[data].mean()),
                style={
                    'width': '50%'
                }
            ),
        )
    ])


def convert_dash_format(layout):
    convert = ()
    for i in range(len(layout)):
        convert += layout[i]
    return convert


def slider_input_update(slider_val, input_val, old_slider_val, old_input_val):
    if slider_val != input_val:
        if slider_val == old_slider_val:
            updated_slider_val = input_val
            updated_input_val = input_val
        else:
            updated_input_val = slider_val
            updated_slider_val = slider_val
        return updated_slider_val, updated_input_val


def check_for_update(slider, input, slider_output, input_output):
    if slider != input:
        slider_updated, input_updated = slider_input_update(
            slider, input, slider_output, input_output)
    else:
        slider_updated = slider
        input_updated = input
    return slider_updated, input_updated
