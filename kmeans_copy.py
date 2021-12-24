#imports
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# dataframe definitions for clustering app
poverty = pd.read_csv('data/poverty.csv', low_memory=False)

#initiating the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server

app.layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Select the year'),
            dcc.Slider(id='year_cluster_slider',
                       dots=True, min=1974, max=2018, step=1, included=False,
                       value=2018,
                       marks={year: str(year)
                              for year in range(1974, 2019, 5)})
        ], lg=5),
        dbc.Col([
            dbc.Label('Select the number of clusters'),
            dcc.Slider(id='ncluster_cluster_slider',
                       dots=True, min=2, max=15, step=1, included=False,
                       value=4,
                       marks={n: str(n) for n in range(2, 16)}),
        ], lg=5),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Select indicators'),
            dcc.Dropdown(id='cluster_indicator_dropdown',
                         optionHeight=30,
                         multi=True,
                         value=['GINI index (World Bank estimate)'],
                         options=[{'label': indicator, 'value': indicator}
                                  for indicator in poverty.columns[3:54]]),
        ], lg=8),
        dbc.Col([
            html.Br(),
            dbc.Button("Submit", id='clustering_submit_button', size="me-1"),
            ], lg=2),
    ]),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dcc.Loading([
                dcc.Graph(id='clustered_map_graph'),
            ]),
        ],lg=10),
    ]),
    html.Br(),
], style={'backgroundColor': '#E5ECF6'})

@app.callback(Output('clustered_map_graph', 'figure'),
              Input('clustering_submit_button', 'n_clicks'),
              State('year_cluster_slider', 'value'),
              State('ncluster_cluster_slider', 'value'),
              State('cluster_indicator_dropdown', 'value'))
def clustered_map(n_clicks, year, n_clusters, indicators):
    if not indicators:
        raise PreventUpdate
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    scaler = StandardScaler()
    kmeans = KMeans(n_clusters=n_clusters)
    df = poverty[poverty['is_country'] & poverty['year'].eq(year)][indicators + ['Country Name', 'year']]
    data = df[indicators]
    if df.isna().all().any():
        return px.scatter(title='No available data for the selected combination of year/indicators.')
    data_no_na = imp.fit_transform(data)
    scaled_data = scaler.fit_transform(data_no_na)
    kmeans.fit(scaled_data)

    fig = px.choropleth(df,
                        locations='Country Name',
                        locationmode='country names',
                        color=[str(x) for x in kmeans.labels_],
                        labels={'color': 'Cluster'},
                        hover_data=indicators,
                        height=650,
                        title=f'Country clusters - {year}.Number of clusters: {n_clusters}<br>Intertia: {kmeans.inertia_:,.2f}',
                        color_discrete_sequence=px.colors.qualitative.T10
                        )
    fig.add_annotation(x=0.01, y=-0.15,
                       xref='paper', yref='paper',
                       text='Selected indicators:<br>' + "<br>".join(indicators),
                       showarrow=False)
    fig.layout.geo.showframe = False
    fig.layout.geo.showcountries = True
    fig.layout.geo.projection.type = 'natural earth'
    fig.layout.geo.lataxis.range = [-53, 76]
    fig.layout.geo.lonaxis.range = [-137, 168]
    fig.layout.geo.landcolor = 'white'
    fig.layout.geo.bgcolor = '#E5ECF6'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.geo.countrycolor = 'gray'
    fig.layout.geo.coastlinecolor = 'gray'
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

