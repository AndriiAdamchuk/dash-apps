# imports
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import re

#dataframe
poverty = pd.read_csv('data/poverty.csv', low_memory=False)

# app instantiation
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# app layout (list of HTML and interactive components)
app.layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Indicator:'),
            dcc.Dropdown(id='hist_indicator_dropdown',
                         value='GINI index (World Bank estimate)',
                         options=[{'label': indicator, 'value': indicator}
                                  for indicator in poverty.columns[3:54]]),
        ], lg=5),
        #dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Years:'),
            dcc.Dropdown(id='hist_multi_year_selector',
                         value=[2015],
                         multi=True,
                         placeholder='Select one or more years',
                         options=[{'label': year, 'value': year}
                                  for year in poverty['year'].drop_duplicates().sort_values()]),
        ], lg=5)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Modify number of bins:'),
            dcc.Slider(id='hist_bins_slider',
                       dots=True, min=0, max=100, step=5, included=False,
                       marks={x: str(x) for x in range(0,105, 5)}),
            dcc.Graph(id='indicator_year_histogram')
            ],lg=10),
    ]),
    html.Br(),

], style={'backgroundColor': '#E5ECF6'}
)

@app.callback(Output('indicator_year_histogram', 'figure'),
              Input('hist_multi_year_selector', 'value'),
              Input('hist_indicator_dropdown', 'value'),
              Input('hist_bins_slider', 'value'))
def display_histogram(years, indicator, nbins):
    if (not years) or (not indicator):
        raise PreventUpdate
    df = poverty[poverty['year'].isin(years) & poverty['is_country']]

    fig = px.histogram(df, x=indicator, facet_col='year', color='year',
                       title=indicator + ' Histogram',
                       nbins=nbins,
                       facet_col_wrap=4, height=700)
    fig.for_each_xaxis(lambda axis: axis.update(title=''))
    fig.add_annotation(text=indicator, x=0.5, y=-0.12, xref='paper', yref='paper', showarrow=False)
    fig.layout.paper_bgcolor = '#E5ECF6'
    return fig

# running the app
if __name__ == '__main__':
    app.run_server(debug=True)