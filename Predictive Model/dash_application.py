import pandas as pd
import plotly.express as px
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

def create_dash_app(flash_app):
    dash_app=dash.Dash(server=flash_app, name="Dashboard" ,url_base_pathname='/dash/')
    dash_app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={})])
    @dash_app.callback([Output(component_id='output_container', component_property='children'),Output(component_id='my_bee_map', component_property='figure')],[Input(component_id='slct_year', component_property='value')])
    def update_graph(option_slctd):
        print(option_slctd)
        print(type(option_slctd))

        container = "The year chosen by user was: {}".format(option_slctd)

        dff = df.copy()
        dff = dff[dff["Year"] == option_slctd]
        dff = dff[dff["Affected by"] == "Varroa_mites"]

        fig = px.bar(
            data_frame=dff,
            x='State',
            y='Pct of Colonies Impacted',
            hover_data=['State', 'Pct of Colonies Impacted'],
            labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
            template='plotly_dark'
        )

        return container, fig

    return dash_app

