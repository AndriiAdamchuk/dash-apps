# imports
import dash
import dash_html_components as html

# app instantiation
app = dash.Dash(__name__)

# app layout (list of HTML and/or interactive components)
app.layout = html.Div([
    html.H1('Hello, world!')
])

# running the app
if __name__ == '__main__':
    app.run_server(debug=True)