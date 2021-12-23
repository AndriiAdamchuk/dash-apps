# imports
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

# app instantiation
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

# app layout (list of HTML and/or interactive components)
app.layout = html.Div([
    html.H1('Poverty and Equity Database!',
            style={'color': 'grey',
                   'fontSize': '35px'}),
    html.H2('The World Bank'),
    dbc.Tabs([
        dbc.Tab([
            html.Ul([
                html.Li('Number of Economies: 170'),
                html.Li('Temporal Coverage: 1974 - 2019'),
                html.Li('Update Frequency: Quarterly'),
                html.Li('Last Updated: March 18, 2020'),
                html.Li(['Source: ',
                    html.A('https://datacatalog.worldbank.org/dataset/poverty-and-equity-database', href='https://datacatalog.worldbank.org/dataset/poverty-and-equity-database')
                    ]),
                ]),
        ], label='Key Facts:'),
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('Book title: Interactive Dashboards and Data Apps with Plotly and Dash'),
                html.Li(['GitHub repo: ',
                    html.A('https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash', href='https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash')
                    ])
                ])
            ], label='Project Info')
        ])
    ])

# running the app
if __name__ == '__main__':
    app.run_server(debug=True)